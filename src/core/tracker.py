"""
tracker.py – Tracks leg extension state and repetition count.
"""

import time


class LegState:
    """
    Tracks the state of a single leg during extension exercises.
    """

    def __init__(self) -> None:
        self.is_extended: bool = False
        self.start_time: float = 0.0
        self.reps: int = 0

    def start_extension(self) -> None:
        """Call when the leg starts extending."""
        self.is_extended = True
        self.start_time = time.time()

    def reset_extension(self) -> None:
        """Reset the leg to unextended state."""
        self.is_extended = False
        self.start_time = 0.0

    def increment_reps(self) -> None:
        """Increment repetition counter."""
        self.reps += 1