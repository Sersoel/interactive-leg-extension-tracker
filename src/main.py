"""
main.py – Entry point for the interactive leg extension exercise system.
"""

import cv2
import time
import mediapipe as mp

from src.utils.pose import is_leg_extended
from src.core.tracker import LegState
from src.utils.audio import init_audio_system, load_victory_sound, play_victory_sound
from src.config import MAX_REPS, LEG_HOLD_THRESHOLD_SEC

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

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("\n Unable to read from camera.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_pose.process(frame_rgb)

    if results.pose_landmarks:
        height, width, _ = frame.shape

        for leg_name, leg_obj in [("left", left_leg), ("right", right_leg)]:
            extended = is_leg_extended(results.pose_landmarks, leg_name, width)

            if extended and not leg_obj.is_extended:
                leg_obj.start_extension()

            elif extended and leg_obj.is_extended:
                hold_time = time.time() - leg_obj.start_time
                if hold_time >= LEG_HOLD_THRESHOLD_SEC:
                    leg_obj.increment_reps()
                    leg_obj.reset_extension()
                    print(f"\n {leg_name.title()} leg: Repetition {leg_obj.reps}/{MAX_REPS}")

            elif not extended:
                leg_obj.reset_extension()

        # Check for completion
        if left_leg.reps >= MAX_REPS and right_leg.reps >= MAX_REPS:
            print("\n Exercise complete!")
            play_victory_sound()
            break

        # Draw landmarks
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
        )

    cv2.imshow("Leg Extension Tracker", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        print("\n Interrupted by user.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()