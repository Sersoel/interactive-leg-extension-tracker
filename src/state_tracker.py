import time
from .constants import LEG_HOLD_THRESHOLD_SEC, MAX_REPS


class LegState:
    def __init__(self):
        self.extended = False
        self.start_time = None
        self.hold_successful = False
        self.reps = 0

    def update(self, is_currently_extended: bool):
        current_time = time.time()

        if is_currently_extended:
            if not self.extended:
                self.start_time = current_time
                self.extended = True
            else:
                duration = current_time - self.start_time
                if duration >= LEG_HOLD_THRESHOLD_SEC and not self.hold_successful:
                    self.hold_successful = True
                    self.reps += 1
        else:
            self.extended = False
            self.start_time = None
            self.hold_successful = False

    def is_finished(self):
        return self.reps >= MAX_REPS
