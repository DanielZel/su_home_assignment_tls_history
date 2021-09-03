from enum import Enum


class TLS(Enum):
    G = 0
    Y = 1
    R = 2


class TLSHistory:
    def __init__(self):
        pass

    def update(self, current_state: TLS):
        pass

    def get_current_state(self) -> TLS:
        """returns the current traffic light state"""
        pass

    def get_last_transition_to_red_timestamp(self) -> float:
        """returns the timestamp of the latest transition from yellow to red"""
        pass
