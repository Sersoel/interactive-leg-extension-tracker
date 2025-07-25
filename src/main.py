"""
main.py – Entry point for the interactive leg extension exercise system.
"""

import cv2
import time
import mediapipe as mp
import pygame

from src.utils.pose import get_center_of_gravity, get_ankle_x
from src.core.tracker import LegState
from src.utils.audio import init_audio_system, load_victory_sound, play_victory_sound
from src.config import MAX_REPS, LEG_HOLD_THRESHOLD_SEC, LEFT_HIP, RIGHT_HIP, LEFT_ANKLE, RIGHT_ANKLE

# === Initialize Modules ===
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose.Pose()
init_audio_system()
load_victory_sound("assets/sounds/victory.mp3")

# Track leg states
left_leg = LegState()
right_leg = LegState()

# Open camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("Leg Extension Tracker", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Leg Extension Tracker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("\n Unable to read from camera.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_pose.process(frame_rgb)

    if results.pose_landmarks:
        height, width, _ = frame.shape

        # === Visibility check ===
        landmarks = results.pose_landmarks.landmark
        if (
            landmarks[LEFT_HIP].visibility < 0.7 or
            landmarks[RIGHT_HIP].visibility < 0.7 or
            landmarks[LEFT_ANKLE].visibility < 0.7 or
            landmarks[RIGHT_ANKLE].visibility < 0.7
        ):
            cv2.putText(
                frame,
                "Ensure your hips and legs are visible",
                (50, height - 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )
            cv2.imshow("Leg Extension Tracker", frame)
            cv2.waitKey(10)
            continue

        cog_x = get_center_of_gravity(results.pose_landmarks)

        for leg_name, leg_obj in [("left", left_leg), ("right", right_leg)]:
            ankle_x = get_ankle_x(results.pose_landmarks, leg_name)
            if ankle_x is None:
                continue

            pixel_distance = abs((ankle_x - cog_x) * width)
            pixel_threshold = 0.15 * width
            percentage = min(int((pixel_distance / pixel_threshold) * 100), 100)

            center = (100, 200) if leg_name == "left" else (width - 100, 200)
            radius = 50
            color = (0, 255, 0) if percentage >= 100 else (0, 165, 255)
            cv2.circle(frame, center, radius, color, 3)
            cv2.putText(
                frame,
                f"{percentage}%",
                (center[0] - 25, center[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
                cv2.LINE_AA
            )

            if percentage >= 100 and not leg_obj.is_extended:
                leg_obj.start_extension()

            elif percentage >= 100 and leg_obj.is_extended:
                hold_time = time.time() - leg_obj.start_time
                if hold_time >= LEG_HOLD_THRESHOLD_SEC:
                    leg_obj.increment_reps()
                    leg_obj.reset_extension()
                    print(f"\n {leg_name.title()} leg: Repetition {leg_obj.reps}/{MAX_REPS}")

            elif percentage < 100:
                leg_obj.reset_extension()

        cv2.putText(
            frame,
            f"Left: {left_leg.reps}/{MAX_REPS}   Right: {right_leg.reps}/{MAX_REPS}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        if left_leg.reps >= MAX_REPS and right_leg.reps >= MAX_REPS:
            print("\n Exercise complete!")
            play_victory_sound()

            cv2.putText(
                frame,
                "Great Job!",
                (int(width / 2) - 150, int(height / 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 0),
                4,
                cv2.LINE_AA
            )

            while pygame.mixer.music.get_busy():
                cv2.imshow("Leg Extension Tracker", frame)
                cv2.waitKey(100)
            break

        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
        )

    cv2.imshow("Leg Extension Tracker", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        print("\n Interrupted by user.")
        break

cap.release()
cv2.destroyAllWindows()