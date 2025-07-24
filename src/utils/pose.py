"""
pose.py – Utilities for extracting pose landmarks and detecting leg extension.
"""

import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from typing import Optional

from src.config import (
    LEFT_ANKLE, RIGHT_ANKLE, LEFT_HIP, RIGHT_HIP, EXTENSION_X_THRESHOLD
)


def get_center_of_gravity(pose_landmarks: NormalizedLandmarkList) -> float:
    """
    Computes the X-coordinate of the body's center of gravity based on hip positions.
    """
    left_hip = pose_landmarks.landmark[LEFT_HIP].x
    right_hip = pose_landmarks.landmark[RIGHT_HIP].x
    return (left_hip + right_hip) / 2.0


def get_ankle_x(pose_landmarks: NormalizedLandmarkList, leg: str) -> Optional[float]:
    """
    Returns the X-coordinate of the given ankle ('left' or 'right').
    """
    if leg == "left":
        return pose_landmarks.landmark[LEFT_ANKLE].x
    elif leg == "right":
        return pose_landmarks.landmark[RIGHT_ANKLE].x
    else:
        return None


def is_leg_extended(
    pose_landmarks: NormalizedLandmarkList,
    leg: str,
    frame_width: int
) -> bool:
    """
    Determines whether the leg is sufficiently extended from the center of gravity.
    """
    cog_x = get_center_of_gravity(pose_landmarks)
    ankle_x = get_ankle_x(pose_landmarks, leg)

    if ankle_x is None:
        return False

    pixel_threshold = EXTENSION_X_THRESHOLD * frame_width
    pixel_distance = abs((ankle_x - cog_x) * frame_width)

    return pixel_distance > pixel_threshold