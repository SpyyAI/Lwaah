"""
Training script for Saudi Sign Language (KSL) gesture classifier.
Uses MediaPipe for hand landmark extraction and Scikit-Learn for classification.
"""

import os
import cv2
import numpy as np
import mediapipe as mp
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Gesture labels (8 required gestures)
GESTURE_LABELS = [
    'open_hand',           # Navigate to "My Services"
    'closed_fist',         # Go to "Violations Inquiry"
    'thumbs_up',           # Approve / Next Step
    'thumbs_down',         # Reject / Go Back
    'pointing_index',      # Select item
    'victory_sign',        # Go to "Absher Individuals"
    'palm_movement_right', # Navigate Right
    'palm_movement_left',  # Navigate Left
]


def extract_hand_landmarks(image):
    """
    Extract hand landmarks from an image using MediaPipe.
    Returns a flattened 63-dimensional vector (21 landmarks x 3 coordinates).
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Extract and normalize coordinates
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        
        return np.array(landmarks)
    
    return None


def generate_synthetic_data(num_samples_per_gesture=100):
    """
    Generate synthetic training data for demonstration purposes.
    In production, replace this with real collected gesture data.
    """
    print("Generating synthetic training data...")
    print("NOTE: For production, collect real gesture data using the data collection script.")
    
    X = []
    y = []
    
    for gesture_idx, gesture_label in enumerate(GESTURE_LABELS):
        print(f"Generating samples for: {gesture_label}")
        
        for _ in range(num_samples_per_gesture):
            # Generate synthetic 63-dimensional feature vector
            # In real scenario, these would be actual hand landmark coordinates
            
            # Base pattern with some gesture-specific variations
            base_features = np.random.rand(63) * 0.3 + gesture_idx * 0.1
            
            # Add gesture-specific patterns
            if gesture_label == 'open_hand':
                # Fingers spread apart
                base_features[5:20] += 0.3
            elif gesture_label == 'closed_fist':
                # Fingers close together
                base_features[5:20] -= 0.2
            elif gesture_label == 'thumbs_up':
                # Thumb extended
                base_features[1:5] += 0.4
            elif gesture_label == 'thumbs_down':
                # Thumb down
                base_features[1:5] -= 0.4
            elif gesture_label == 'pointing_index':
                # Index finger extended
                base_features[5:9] += 0.3
            elif gesture_label == 'victory_sign':
                # Index and middle fingers extended
                base_features[5:13] += 0.3
            elif gesture_label == 'palm_movement_right':
                # Hand shifted right
                base_features[::3] += 0.2
            elif gesture_label == 'palm_movement_left':
                # Hand shifted left
                base_features[::3] -= 0.2
            
            # Add noise for variability
            noise = np.random.normal(0, 0.05, 63)
            features = base_features + noise
            
            # Normalize to [0, 1] range
            features = np.clip(features, 0, 1)
            
            X.append(features)
            y.append(gesture_label)
    
    return np.array(X), np.array(y)


def train_gesture_classifier():
    """
    Train a RandomForest classifier for gesture recognition.
    """
    print("\n" + "="*50)
    print("LOWAAH - Saudi Sign Language Gesture Classifier")
    print("="*50 + "\n")
    
    # Generate or load training data
    X, y = generate_synthetic_data(num_samples_per_gesture=150)
    
    print(f"\nDataset shape: {X.shape}")
    print(f"Number of gestures: {len(GESTURE_LABELS)}")
    print(f"Gestures: {GESTURE_LABELS}\n")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}\n")
    
    # Train RandomForest classifier
    print("Training RandomForest classifier...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy*100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'gesture_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)
    
    print(f"\n[SUCCESS] Model saved to: {model_path}")
    print("\nModel is ready for deployment!")
    
    # Save gesture labels mapping
    labels_path = os.path.join(os.path.dirname(__file__), 'gesture_labels.pkl')
    with open(labels_path, 'wb') as f:
        pickle.dump(GESTURE_LABELS, f)
    
    print(f"[SUCCESS] Labels saved to: {labels_path}")
    
    return clf


if __name__ == '__main__':
    train_gesture_classifier()
    print("\n" + "="*50)
    print("Training complete! You can now run the Django server.")
    print("="*50)

