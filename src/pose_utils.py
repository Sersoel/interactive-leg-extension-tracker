import math
from typing import Optional
from mediapipe.framework.formats import landmark_pb2
from .constants import LEFT_ANKLE, RIGHT_ANKLE, LEFT_HIP, RIGHT_HIP, EXTENSION_X_THRESHOLD


def get_center_of_gravity(landmarks: landmark_pb2.NormalizedLandmarkList) -> Optional[float]:
    try:
        left_hip = landmarks.landmark[LEFT_HIP].x
        right_hip = landmarks.landmark[RIGHT_HIP].x
        return (left_hip + right_hip) / 2
    except (IndexError, AttributeError):
        return None


def get_ankle_x(landmarks: landmark_pb2.NormalizedLandmarkList, side: str) -> Optional[float]:
    try:
        if side == "left":
            return landmarks.landmark[LEFT_ANKLE].x
        elif side == "right":
            return landmarks.landmark[RIGHT_ANKLE].x
    except (IndexError, AttributeError):
        return None
    return None


def is_leg_extended(ankle_x: float, cog_x: float, side: str) -> bool:
    if side == "left":
        return (cog_x - ankle_x) > EXTENSION_X_THRESHOLD
    elif side == "right":
        return (ankle_x - cog_x) > EXTENSION_X_THRESHOLD
    return False