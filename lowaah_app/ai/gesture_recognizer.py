"""
Rule-based gesture recognition for Saudi Sign Language gestures.
Uses MediaPipe hand landmarks to detect specific hand poses geometrically.
More reliable than ML models trained on synthetic data.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple


class RuleBasedGestureRecognizer:
    """
    Detects gestures using geometric rules on MediaPipe hand landmarks.
    """
    
    def __init__(self):
        """Initialize MediaPipe Hands."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,  # Balanced for accuracy
            min_tracking_confidence=0.5    # Balanced for stable tracking
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Smoothing buffer (optimized for balance between speed and accuracy)
        self.prediction_buffer = []
        self.buffer_size = 5  # Reduced from 7 for faster response
        
        # MediaPipe hand landmark indices
        self.WRIST = 0
        self.THUMB_TIP = 4
        self.THUMB_IP = 3
        self.THUMB_MCP = 2
        self.INDEX_TIP = 8
        self.INDEX_DIP = 7
        self.INDEX_PIP = 6
        self.INDEX_MCP = 5
        self.MIDDLE_TIP = 12
        self.MIDDLE_PIP = 10
        self.RING_TIP = 16
        self.RING_PIP = 14
        self.PINKY_TIP = 20
        self.PINKY_PIP = 18
    
    def clear_buffer(self):
        """Clear the prediction buffer. Call this when starting a new detection session."""
        self.prediction_buffer = []
        print("🧹 Gesture buffer cleared")
    
    def get_distance(self, p1, p2):
        """Calculate Euclidean distance between two landmarks."""
        return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
    
    def is_finger_extended(self, landmarks, tip_idx, pip_idx, mcp_idx=None):
        """Check if a finger is extended based on tip-to-pip distance."""
        tip = landmarks[tip_idx]
        pip = landmarks[pip_idx]
        
        if mcp_idx:
            mcp = landmarks[mcp_idx]
            # Finger is extended if tip is farther from wrist than PIP
            wrist = landmarks[self.WRIST]
            tip_dist = self.get_distance(tip, wrist)
            pip_dist = self.get_distance(pip, wrist)
            return tip_dist > pip_dist
        else:
            # Simple check: tip is above (smaller y) than pip
            return tip.y < pip.y
    
    def is_finger_closed(self, landmarks, tip_idx, pip_idx):
        """Check if a finger is closed/bent."""
        return not self.is_finger_extended(landmarks, tip_idx, pip_idx)
    
    def detect_open_hand(self, landmarks):
        """Detect open hand - all fingers extended, palm forward."""
        fingers_extended = [
            self.is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP),
            self.is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP),
            self.is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        ]
        
        # Thumb should also be somewhat extended (not tucked)
        thumb_tip = landmarks[self.THUMB_TIP]
        wrist = landmarks[self.WRIST]
        thumb_dist = self.get_distance(thumb_tip, wrist)
        thumb_extended = thumb_dist > 0.15
        
        # ALL 4 fingers extended AND thumb not tucked
        return sum(fingers_extended) == 4 and thumb_extended
    
    def detect_pinky_extended(self, landmarks):
        """Detect pinky extended (rock sign 🤘) - pinky and index up, middle and ring down."""
        # Check pinky is extended
        pinky_extended = self.is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        
        # Check index is extended (for rock sign variation)
        index_extended = self.is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP)
        
        # Check middle and ring are closed
        middle_closed = self.is_finger_closed(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_closed = self.is_finger_closed(landmarks, self.RING_TIP, self.RING_PIP)
        
        # Rock sign: pinky + index extended, middle + ring closed
        return pinky_extended and index_extended and middle_closed and ring_closed
    
    def detect_closed_fist(self, landmarks):
        """DEPRECATED - Kept for backward compatibility. Use detect_pinky_extended instead."""
        # Fallback to pinky extended detection
        return self.detect_pinky_extended(landmarks)
    
    def detect_thumbs_up(self, landmarks):
        """Detect thumbs up - thumb extended upward, others closed."""
        thumb_tip = landmarks[self.THUMB_TIP]
        thumb_ip = landmarks[self.THUMB_IP]
        thumb_mcp = landmarks[self.THUMB_MCP]
        wrist = landmarks[self.WRIST]
        index_mcp = landmarks[self.INDEX_MCP]
        
        # Thumb extended upward (y coordinate smaller = higher on screen)
        thumb_up = thumb_tip.y < thumb_ip.y and thumb_tip.y < thumb_mcp.y
        
        # Thumb should be above wrist AND above hand (relaxed threshold)
        thumb_high = thumb_tip.y < wrist.y - 0.08 and thumb_tip.y < index_mcp.y  # Relaxed from 0.15
        
        # Thumb should be pointing upward (relaxed for more tolerance)
        thumb_vertical = abs(thumb_tip.x - thumb_ip.x) < 0.15  # Relaxed from 0.1
        
        # All other fingers must be closed
        fingers_closed = [
            self.is_finger_closed(landmarks, self.INDEX_TIP, self.INDEX_PIP),
            self.is_finger_closed(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.is_finger_closed(landmarks, self.RING_TIP, self.RING_PIP),
            self.is_finger_closed(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        ]
        
        return thumb_up and thumb_high and thumb_vertical and sum(fingers_closed) == 4
    
    def detect_thumbs_down(self, landmarks):
        """Detect thumbs down - thumb pointing down, others closed."""
        thumb_tip = landmarks[self.THUMB_TIP]
        thumb_ip = landmarks[self.THUMB_IP]
        thumb_mcp = landmarks[self.THUMB_MCP]
        wrist = landmarks[self.WRIST]
        index_mcp = landmarks[self.INDEX_MCP]
        
        # Thumb pointing down (tip lower than IP and MCP)
        thumb_down = thumb_tip.y > thumb_ip.y and thumb_tip.y > thumb_mcp.y
        
        # Thumb should be below the hand/wrist
        thumb_low = thumb_tip.y > wrist.y + 0.05 and thumb_tip.y > index_mcp.y
        
        # Thumb should be pointing downward (not sideways)
        thumb_vertical = abs(thumb_tip.x - thumb_ip.x) < 0.1
        
        # All other fingers must be closed
        fingers_closed = [
            self.is_finger_closed(landmarks, self.INDEX_TIP, self.INDEX_PIP),
            self.is_finger_closed(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.is_finger_closed(landmarks, self.RING_TIP, self.RING_PIP),
            self.is_finger_closed(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        ]
        
        return thumb_down and thumb_low and thumb_vertical and sum(fingers_closed) == 4
    
    def detect_pointing_index(self, landmarks):
        """Detect pointing with index finger - only index extended."""
        index_extended = self.is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP)
        middle_extended = self.is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        
        # Make sure ONLY index is extended, not middle
        others_closed = [
            self.is_finger_closed(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.is_finger_closed(landmarks, self.RING_TIP, self.RING_PIP),
            self.is_finger_closed(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        ]
        
        return index_extended and not middle_extended and sum(others_closed) == 3
    
    def detect_victory_sign(self, landmarks):
        """Detect victory/peace sign - index and middle fingers extended, others closed."""
        index_extended = self.is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP)
        middle_extended = self.is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_extended = self.is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
        
        # Ring and pinky must be closed
        others_closed = [
            self.is_finger_closed(landmarks, self.RING_TIP, self.RING_PIP),
            self.is_finger_closed(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        ]
        
        # ONLY index and middle extended, NOT ring
        return index_extended and middle_extended and not ring_extended and sum(others_closed) == 2
    
    def detect_palm_movement(self, landmarks):
        """Detect palm movement direction based on hand position."""
        wrist = landmarks[self.WRIST]
        middle_mcp = landmarks[9]  # Middle finger base
        
        # Calculate horizontal offset
        horizontal_offset = middle_mcp.x - wrist.x
        
        if horizontal_offset > 0.1:
            return 'swipe_right'
        elif horizontal_offset < -0.1:
            return 'swipe_left'
        
        return None
    
    def detect_swipe_left(self, landmarks) -> bool:
        """Detect horizontal swipe left for backspace."""
        wrist = landmarks[self.WRIST]
        index_tip = landmarks[self.INDEX_TIP]
        
        # Hand moving significantly to the left
        horizontal_movement = index_tip.x - wrist.x
        return horizontal_movement < -0.2  # Strong left movement
    
    def detect_backspace(self, landmarks) -> bool:
        """Detect backspace gesture - pinky extended alone or swipe left."""
        # Option 1: Only pinky extended
        pinky_extended = self.is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        others_closed = [
            self.is_finger_closed(landmarks, self.INDEX_TIP, self.INDEX_PIP),
            self.is_finger_closed(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.is_finger_closed(landmarks, self.RING_TIP, self.RING_PIP)
        ]
        
        if pinky_extended and sum(others_closed) >= 3:
            return True
        
        # Option 2: Swipe left
        return self.detect_swipe_left(landmarks)
    
    def detect_three_fingers(self, landmarks) -> bool:
        """
        Detect three fingers up (index + middle + ring extended, pinky + thumb down).
        🖖 Three Fingers → Show Settings/Help
        """
        # Check index, middle, ring are extended
        index_extended = self.is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP, self.INDEX_MCP)
        middle_extended = self.is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_extended = self.is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
        
        # Check pinky and thumb are NOT extended
        pinky_extended = self.is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        
        # Thumb check: tip should be far from palm center
        thumb_tip = landmarks[self.THUMB_TIP]
        wrist = landmarks[self.WRIST]
        thumb_extended = self.get_distance(thumb_tip, wrist) > 0.15
        
        # All three middle fingers up, pinky and thumb down
        if index_extended and middle_extended and ring_extended and not pinky_extended and not thumb_extended:
            return True
        
        return False
    
    def detect_ok_sign(self, landmarks) -> bool:
        """
        Detect OK sign (thumb tip touching index tip, other fingers extended).
        👌 OK Sign → Open Profile
        """
        # Get thumb tip and index tip landmarks
        thumb_tip = landmarks[self.THUMB_TIP]
        index_tip = landmarks[self.INDEX_TIP]
        
        # Calculate distance between thumb and index tips
        distance = self.get_distance(thumb_tip, index_tip)
        
        # Check if tips are close (touching)
        if distance < 0.06:  # Threshold for "touching"
            # Check other fingers are extended
            middle_extended = self.is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
            ring_extended = self.is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
            pinky_extended = self.is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
            
            # At least 2 of the 3 other fingers should be extended
            extended_count = sum([middle_extended, ring_extended, pinky_extended])
            if extended_count >= 2:
                return True
        
        return False
    
    def recognize_gesture(self, landmarks) -> Optional[str]:
        """
        Recognize gesture from hand landmarks using rule-based detection.
        Priority order: most specific gestures first.
        """
        # Check OK sign first (very specific - thumb + index touching)
        if self.detect_ok_sign(landmarks):
            return 'ok_sign'
        
        # Check three fingers (specific combination)
        if self.detect_three_fingers(landmarks):
            return 'three_fingers'
        
        # Check backspace (very specific - pinky only down)
        if self.detect_backspace(landmarks):
            return 'backspace'
        
        # Check pinky extended / rock sign (pinky + index up, others down)
        if self.detect_pinky_extended(landmarks):
            return 'closed_fist'  # Return 'closed_fist' for backward compatibility
        
        # Check thumbs gestures (very specific)
        if self.detect_thumbs_up(landmarks):
            return 'thumbs_up'
        
        if self.detect_thumbs_down(landmarks):
            return 'thumbs_down'
        
        # Check specific finger combinations
        if self.detect_victory_sign(landmarks):
            return 'victory_sign'
        
        if self.detect_pointing_index(landmarks):
            return 'pointing_index'
        
        # Check open hand (less specific)
        if self.detect_open_hand(landmarks):
            return 'open_hand'
        
        # NOTE: Palm movement (swipe_left/swipe_right) disabled to avoid conflicts
        # with thumbs_up and other gestures. Use open_hand + movement detection
        # in frontend if needed.
        
        return None
    
    def predict_gesture(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Predict gesture from an image.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (gesture_label, confidence) or (None, 0.0) if no hand detected
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = hand_landmarks.landmark
            
            # Recognize gesture
            gesture = self.recognize_gesture(landmarks)
            
            if gesture:
                # Add to buffer for smoothing
                self.prediction_buffer.append(gesture)
                if len(self.prediction_buffer) > self.buffer_size:
                    self.prediction_buffer.pop(0)
                
                # Use most common prediction in buffer (optimized for speed + accuracy)
                if len(self.prediction_buffer) >= 3:  # Reduced to 3 for faster response
                    from collections import Counter
                    gesture_counts = Counter(self.prediction_buffer)
                    most_common_gesture, count = gesture_counts.most_common(1)[0]
                    
                    # Only return gesture if it appears in at least 60% of buffer (balanced threshold)
                    min_required = max(2, int(len(self.prediction_buffer) * 0.6))
                    if count >= min_required:
                        gesture = most_common_gesture
                        confidence = count / len(self.prediction_buffer)
                        return gesture, confidence
                    else:
                        # Not stable enough, don't return anything
                        return None, 0.0
                else:
                    # Not enough samples yet
                    return None, 0.0
            
        return None, 0.0
    
    def draw_landmarks(self, image: np.ndarray) -> np.ndarray:
        """Draw hand landmarks on the image."""
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

