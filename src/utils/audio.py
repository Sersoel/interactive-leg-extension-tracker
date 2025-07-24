"""
audio.py – Handles audio playback using pygame.
"""

import pygame
import os


def init_audio_system() -> None:
    """Initializes the Pygame mixer."""
    pygame.mixer.init()


def load_victory_sound(sound_path: str) -> None:
    """
    Loads a sound file into memory.
    
    Args:
        sound_path: Path to the victory sound ("assets/sounds/victory.mp3")
    """
    if not os.path.exists(sound_path):
        raise FileNotFoundError(f"Sound file not found: {sound_path}")
    pygame.mixer.music.load(sound_path)


def play_victory_sound() -> None:
    """Plays the victory sound."""
    pygame.mixer.music.play()