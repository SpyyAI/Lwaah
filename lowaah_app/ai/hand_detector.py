"""
Hand Detector module for real-time gesture recognition using MediaPipe and Scikit-Learn.
Processes frames and predicts Saudi Sign Language (KSL) gestures.
"""

import cv2
import numpy as np
import mediapipe as mp
import pickle
import os
from typing import Optional, Tuple


class HandGestureDetector:
    """
    Detects and classifies hand gestures using MediaPipe and a trained ML model.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the hand gesture detector.
        
        Args:
            model_path: Path to the trained gesture classification model (.pkl)
        """
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Load trained model
        self.model = None
        self.gesture_labels = None
        self.load_model(model_path)
        
        # Smoothing buffer for stable predictions
        self.prediction_buffer = []
        self.buffer_size = 5
    
    def load_model(self, model_path: str):
        """Load the trained gesture classification model."""
        try:
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✅ Gesture model loaded from: {model_path}")
                
                # Load gesture labels
                labels_path = model_path.replace('gesture_model.pkl', 'gesture_labels.pkl')
                if os.path.exists(labels_path):
                    with open(labels_path, 'rb') as f:
                        self.gesture_labels = pickle.load(f)
                    print(f"✅ Gesture labels loaded: {self.gesture_labels}")
                else:
                    # Default labels
                    self.gesture_labels = [
                        'open_hand', 'closed_fist', 'thumbs_up', 'thumbs_down',
                        'pointing_index', 'victory_sign', 'palm_movement_right', 'palm_movement_left'
                    ]
            else:
                print(f"⚠️ Model file not found: {model_path}")
                print("Please run: python lowaah_app/ai/train_model.py")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    
    def extract_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand landmarks from an image.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Normalized landmark coordinates as 63-dimensional array, or None if no hand detected
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract coordinates
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            
            return np.array(landmarks).reshape(1, -1)
        
        return None
    
    def predict_gesture(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Predict gesture from an image.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (gesture_label, confidence) or (None, 0.0) if no hand detected
        """
        if self.model is None:
            return None, 0.0
        
        # Extract landmarks
        landmarks = self.extract_landmarks(image)
        
        if landmarks is None:
            return None, 0.0
        
        # Predict gesture
        try:
            prediction = self.model.predict(landmarks)
            probabilities = self.model.predict_proba(landmarks)
            confidence = np.max(probabilities)
            gesture = prediction[0]
            
            # Add to buffer for smoothing
            self.prediction_buffer.append(gesture)
            if len(self.prediction_buffer) > self.buffer_size:
                self.prediction_buffer.pop(0)
            
            # Use most common prediction in buffer
            if len(self.prediction_buffer) >= 3:
                from collections import Counter
                gesture = Counter(self.prediction_buffer).most_common(1)[0][0]
            
            return gesture, confidence
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, 0.0
    
    def draw_landmarks(self, image: np.ndarray) -> np.ndarray:
        """
        Draw hand landmarks on the image.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Image with landmarks drawn
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        return image
    
    def process_frame(self, image: np.ndarray) -> dict:
        """
        Process a frame and return gesture detection results.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Dictionary with gesture, confidence, and annotated image
        """
        # Make a copy for annotation
        annotated_image = image.copy()
        
        # Predict gesture
        gesture, confidence = self.predict_gesture(image)
        
        # Draw landmarks
        annotated_image = self.draw_landmarks(annotated_image)
        
        # Add gesture text
        if gesture:
            text = f"{gesture} ({confidence*100:.1f}%)"
            cv2.putText(
                annotated_image, 
                text, 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 255, 0), 
                2
            )
        else:
            cv2.putText(
                annotated_image, 
                "No hand detected", 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 0, 255), 
                2
            )
        
        return {
            'gesture': gesture,
            'confidence': confidence,
            'image': annotated_image
        }
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'hands'):
            self.hands.close()


def test_detector():
    """Test the detector with webcam."""
    import sys
    
    # Get model path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'gesture_model.pkl')
    
    # Initialize detector
    detector = HandGestureDetector(model_path)
    
    if detector.model is None:
        print("❌ Model not loaded. Please train the model first:")
        print("   python lowaah_app/ai/train_model.py")
        sys.exit(1)
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        sys.exit(1)
    
    print("✅ Webcam opened. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        result = detector.process_frame(frame)
        
        # Display
        cv2.imshow('Lowaah - Gesture Detection Test', result['image'])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test_detector()

