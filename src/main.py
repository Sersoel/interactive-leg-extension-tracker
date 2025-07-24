import cv2
import mediapipe as mp
import pygame

from src.pose_utils import get_center_of_gravity, get_ankle_x, is_leg_extended
from src.state_tracker import LegState
from src.constants import MAX_REPS

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/victory.mp3")

# Track leg states
left_leg = LegState()
right_leg = LegState()

# OpenCV video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cog_x = get_center_of_gravity(results.pose_landmarks)
        left_ankle_x = get_ankle_x(results.pose_landmarks, "left")
        right_ankle_x = get_ankle_x(results.pose_landmarks, "right")

        if cog_x is not None and left_ankle_x is not None and right_ankle_x is not None:
            left_extended = is_leg_extended(left_ankle_x, cog_x, "left")
            right_extended = is_leg_extended(right_ankle_x, cog_x, "right")

            left_leg.update(left_extended)
            right_leg.update(right_extended)

            cv2.putText(frame, f"Left Reps: {left_leg.reps}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Right Reps: {right_leg.reps}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if left_extended:
                cv2.putText(frame, "Left Leg Extended", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if right_extended:
                cv2.putText(frame, "Right Leg Extended", (10, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            if left_leg.is_finished() and right_leg.is_finished():
                cv2.putText(frame, "Exercise Complete!", (10, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()

    cv2.imshow("Leg Extension Tracker", frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()