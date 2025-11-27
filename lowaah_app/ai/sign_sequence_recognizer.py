"""
Sign Language Sequence Recognition using LSTM/Transformer
Captures temporal sequences of hand gestures and translates to text.

Architecture:
- MediaPipe hand tracking → Extract 21 landmarks (x, y, z) × 2 hands = 126 features
- Sequence buffer → Store last N frames
- LSTM model → Process temporal sequences
- Output → Predicted word/phrase
"""

import numpy as np
import cv2
import mediapipe as mp
from typing import Optional, List, Tuple, Dict
import pickle
import os
from collections import deque

try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow not available. Using rule-based fallback.")


class SignSequenceRecognizer:
    """
    Real-time sign language sequence recognition.
    Processes sequences of hand landmarks to recognize signs.
    """
    
    def __init__(self, model_path: str = None, use_lstm: bool = True):
        """
        Initialize the sign sequence recognizer.
        
        Args:
            model_path: Path to pre-trained LSTM model (optional)
            use_lstm: Whether to use LSTM model (requires TensorFlow)
        """
        # MediaPipe Hands setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,  # Support two hands for complex signs
            min_detection_confidence=0.3,  # LOWERED - easier hand detection
            min_tracking_confidence=0.3    # LOWERED - easier tracking
        )
        
        # Sequence parameters
        self.sequence_length = 30  # Number of frames to analyze (1 second at 30fps)
        self.landmark_sequence = deque(maxlen=self.sequence_length)
        
        # Feature dimensions
        self.num_landmarks_per_hand = 21
        self.coords_per_landmark = 3  # x, y, z
        self.max_hands = 2
        self.feature_size = self.num_landmarks_per_hand * self.coords_per_landmark * self.max_hands  # 126
        
        # Model
        self.use_lstm = use_lstm and TENSORFLOW_AVAILABLE
        self.model = None
        self.label_encoder = None
        
        if self.use_lstm and model_path and os.path.exists(model_path):
            self.load_model(model_path)
        
        # Vocabulary for recognition
        from .sign_language_vocabulary import COMPLETE_VOCABULARY
        self.vocabulary = COMPLETE_VOCABULARY
        
        # Text buffer (for building sentences)
        self.recognized_words = []
        self.current_text = ""
        
        # Detection state
        self.last_sign = None
        self.sign_stable_count = 0
        self.stability_threshold = 15  # Frames needed for confirmation
        
        print(f"✅ SignSequenceRecognizer initialized (LSTM: {self.use_lstm})")
    
    def extract_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand landmarks from image.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Flattened array of landmarks [126 features] or None
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.hands.process(image_rgb)
        
        # Initialize feature array (filled with zeros for missing hands)
        features = np.zeros(self.feature_size)
        
        if results.multi_hand_landmarks:
            # Process up to 2 hands
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks[:2]):
                # Extract landmarks
                landmarks_array = []
                for landmark in hand_landmarks.landmark:
                    landmarks_array.extend([landmark.x, landmark.y, landmark.z])
                
                # Place in feature array
                start_idx = hand_idx * self.num_landmarks_per_hand * self.coords_per_landmark
                end_idx = start_idx + len(landmarks_array)
                features[start_idx:end_idx] = landmarks_array
            
            return features
        
        return None
    
    def add_frame(self, image: np.ndarray) -> bool:
        """
        Add a frame to the sequence buffer.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            True if landmarks were detected, False otherwise
        """
        landmarks = self.extract_landmarks(image)
        
        if landmarks is not None:
            self.landmark_sequence.append(landmarks)
            return True
        else:
            # Add zeros for missing frames (maintain temporal continuity)
            self.landmark_sequence.append(np.zeros(self.feature_size))
            return False
    
    def predict_sequence(self) -> Tuple[Optional[str], float]:
        """
        Predict sign from current sequence buffer.
        
        Returns:
            Tuple of (predicted_sign, confidence)
        """
        # Need minimum sequence length
        if len(self.landmark_sequence) < self.sequence_length:
            return None, 0.0
        
        # Convert sequence to numpy array
        sequence_array = np.array(list(self.landmark_sequence))
        
        # Reshape for LSTM input: (1, sequence_length, features)
        sequence_reshaped = sequence_array.reshape(1, self.sequence_length, self.feature_size)
        
        if self.use_lstm and self.model is not None:
            # Use trained LSTM model
            try:
                predictions = self.model.predict(sequence_reshaped, verbose=0)
                predicted_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_idx])
                
                if self.label_encoder:
                    predicted_sign = self.label_encoder[predicted_idx]
                    return predicted_sign, confidence
                
            except Exception as e:
                print(f"⚠️ LSTM prediction error: {e}")
        
        # Fallback: Rule-based recognition using latest frame
        return self._rule_based_recognition()
    
    def _rule_based_recognition(self) -> Tuple[Optional[str], float]:
        """
        Fallback rule-based recognition for when LSTM is unavailable.
        Uses geometric patterns from the latest frame.
        """
        if len(self.landmark_sequence) == 0:
            return None, 0.0
        
        # Get latest frame
        latest_landmarks = self.landmark_sequence[-1]
        
        # Simple pattern matching (expandable)
        # This is a simplified version - you would add more sophisticated rules
        
        # Check if hand is present (non-zero landmarks)
        if np.sum(np.abs(latest_landmarks)) < 0.1:
            return None, 0.0
        
        # Example: Detect static poses based on finger configurations
        # (This would be expanded with actual KSL sign patterns)
        
        return "unknown", 0.5
    
    def recognize_continuous(self, image: np.ndarray) -> Dict:
        """
        Continuous recognition from video stream.
        Handles sign stability and word building.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Dictionary with recognition results
        """
        # Add frame to sequence
        hand_detected = self.add_frame(image)
        
        if not hand_detected:
            # Reset if no hand detected for a while
            self.sign_stable_count = 0
            return {
                'sign': None,
                'confidence': 0.0,
                'text': self.current_text,
                'status': 'no_hand_detected'
            }
        
        # Predict from sequence
        predicted_sign, confidence = self.predict_sequence()
        
        if predicted_sign is None or confidence < 0.6:
            self.sign_stable_count = 0
            return {
                'sign': None,
                'confidence': confidence,
                'text': self.current_text,
                'status': 'uncertain'
            }
        
        # Check sign stability (same sign detected multiple times)
        if predicted_sign == self.last_sign:
            self.sign_stable_count += 1
        else:
            self.last_sign = predicted_sign
            self.sign_stable_count = 1
        
        # Confirm sign if stable
        if self.sign_stable_count >= self.stability_threshold:
            # Add to recognized words
            self.recognized_words.append(predicted_sign)
            self.current_text = ' '.join(self.recognized_words)
            
            # Reset for next sign
            self.sign_stable_count = 0
            self.last_sign = None
            self.landmark_sequence.clear()
            
            return {
                'sign': predicted_sign,
                'confidence': confidence,
                'text': self.current_text,
                'status': 'confirmed',
                'word_added': True
            }
        
        return {
            'sign': predicted_sign,
            'confidence': confidence,
            'text': self.current_text,
            'status': 'detecting',
            'stability': self.sign_stable_count / self.stability_threshold
        }
    
    def clear_text(self):
        """Clear the recognized text buffer."""
        self.recognized_words.clear()
        self.current_text = ""
        self.landmark_sequence.clear()
        self.last_sign = None
        self.sign_stable_count = 0
    
    def delete_last_word(self):
        """Delete the last recognized word (backspace)."""
        if self.recognized_words:
            self.recognized_words.pop()
            self.current_text = ' '.join(self.recognized_words)
    
    def load_model(self, model_path: str):
        """Load pre-trained LSTM model."""
        try:
            if not TENSORFLOW_AVAILABLE:
                print("⚠️ TensorFlow not available. Cannot load LSTM model.")
                return False
            
            self.model = load_model(model_path)
            
            # Load label encoder
            label_path = model_path.replace('.h5', '_labels.pkl')
            if os.path.exists(label_path):
                with open(label_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
            
            print(f"✅ LSTM model loaded from {model_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def build_and_train_model(self, X_train: np.ndarray, y_train: np.ndarray, 
                              num_classes: int, epochs: int = 50):
        """
        Build and train LSTM model from scratch.
        
        Args:
            X_train: Training sequences (samples, sequence_length, features)
            y_train: Training labels (one-hot encoded)
            num_classes: Number of sign classes
            epochs: Training epochs
        """
        if not TENSORFLOW_AVAILABLE:
            print("❌ TensorFlow required for training")
            return None
        
        print("🏗️ Building LSTM model...")
        
        model = Sequential([
            # Bidirectional LSTM layers
            Bidirectional(LSTM(128, return_sequences=True, 
                              input_shape=(self.sequence_length, self.feature_size))),
            Dropout(0.3),
            
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.3),
            
            Bidirectional(LSTM(32)),
            Dropout(0.3),
            
            # Dense layers
            Dense(64, activation='relu'),
            Dropout(0.2),
            
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("📊 Model architecture:")
        model.summary()
        
        # Train model
        print(f"🎯 Training for {epochs} epochs...")
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )
        
        self.model = model
        print("✅ Model training complete!")
        
        return model, history
    
    def save_model(self, save_path: str):
        """Save trained model."""
        if self.model is None:
            print("❌ No model to save")
            return False
        
        try:
            self.model.save(save_path)
            
            # Save label encoder
            if self.label_encoder:
                label_path = save_path.replace('.h5', '_labels.pkl')
                with open(label_path, 'wb') as f:
                    pickle.dump(self.label_encoder, f)
            
            print(f"✅ Model saved to {save_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save model: {e}")
            return False
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'hands'):
            self.hands.close()


# ============================================================================
# TRAINING UTILITY FUNCTIONS
# ============================================================================

def create_synthetic_training_data(num_samples: int = 1000, 
                                   num_classes: int = 50,
                                   sequence_length: int = 30,
                                   feature_size: int = 126):
    """
    Create synthetic training data for initial model.
    In production, replace with real sign language video data.
    
    Args:
        num_samples: Number of training samples
        num_classes: Number of sign classes
        sequence_length: Length of each sequence
        feature_size: Number of features per frame
        
    Returns:
        X_train, y_train, label_encoder
    """
    print(f"🔧 Creating synthetic training data...")
    print(f"   Samples: {num_samples}, Classes: {num_classes}")
    
    # Generate random sequences (replace with real data)
    X = np.random.randn(num_samples, sequence_length, feature_size)
    
    # Generate random labels
    y = np.random.randint(0, num_classes, size=num_samples)
    
    # One-hot encode labels
    from tensorflow.keras.utils import to_categorical
    y_encoded = to_categorical(y, num_classes)
    
    # Create label encoder (sign names)
    from .sign_language_vocabulary import ABSHER_SERVICES, ACTION_VERBS, COMMON_PHRASES
    all_signs = list(ABSHER_SERVICES.keys())[:num_classes]
    label_encoder = {i: sign for i, sign in enumerate(all_signs)}
    
    print(f"✅ Synthetic data created: X shape={X.shape}, y shape={y_encoded.shape}")
    
    return X, y_encoded, label_encoder


if __name__ == "__main__":
    """
    Training script example.
    """
    print("=" * 60)
    print("Sign Language Sequence Recognizer - Training Mode")
    print("=" * 60)
    
    if not TENSORFLOW_AVAILABLE:
        print("❌ TensorFlow not installed. Please run:")
        print("   pip install tensorflow")
        exit(1)
    
    # Create recognizer
    recognizer = SignSequenceRecognizer(use_lstm=True)
    
    # Create synthetic training data (replace with real data)
    X_train, y_train, label_encoder = create_synthetic_training_data(
        num_samples=1000,
        num_classes=50,
        sequence_length=recognizer.sequence_length,
        feature_size=recognizer.feature_size
    )
    
    recognizer.label_encoder = label_encoder
    
    # Train model
    model, history = recognizer.build_and_train_model(
        X_train, y_train,
        num_classes=50,
        epochs=20  # Reduce for faster training
    )
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'sign_lstm_model.h5')
    recognizer.save_model(model_path)
    
    print("\n" + "=" * 60)
    print("✅ Training complete! Model saved.")
    print("=" * 60)

