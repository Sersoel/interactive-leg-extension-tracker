"""
config.py – Configuration constants used throughout the leg extension project.
"""

# MediaPipe landmark indices
# https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HIP = 23
RIGHT_HIP = 24

# Pose detection thresholds
LEG_HOLD_THRESHOLD_SEC = 3.0     # Minimum hold duration (seconds)
EXTENSION_X_THRESHOLD = 0.15     # X distance threshold (as fraction of frame width)

# Repetition limit
MAX_REPS = 5