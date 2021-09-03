import random
from time import sleep, time
from threading import Thread
from queue import Queue

from tls_history import TLSHistory, TLS

# TLS = Traffic Light State
CAR_STATE_UPDATE_RATE = 10  # HZ
TLS_TRANSITION_RATE = 3  # HZ
TLS_MIN_TIME = 3  # sec
TLS_MAX_TIME = 8  # sec


class TLSSimulatorThread(Thread):
    def __init__(self, tls_history):
        super(TLSSimulatorThread, self).__init__(daemon=True)
        self.tls_history = tls_history

    def run(self):
        current_state = TLS.G
        transition_ts = time() + random.randint(TLS_MIN_TIME, TLS_MAX_TIME)

        while True:
            if time() > transition_ts:
                transition_ts = time() + random.randint(TLS_MIN_TIME, TLS_MAX_TIME)
                current_state = TLS((current_state.value + 1) % len(TLS))

            self.tls_history.update(current_state)
            sleep(1/TLS_TRANSITION_RATE)


class CarSimulatorThread(Thread):
    def __init__(self, q: Queue):
        super(CarSimulatorThread, self).__init__(daemon=True)
        self.q = q

    def run(self):
        has_crossed = False
        crossing_time = time() + random.randint(5, 10)
        while True:
            if time() > crossing_time:
                has_crossed = True
            self.q.put(has_crossed)
            sleep(1 / CAR_STATE_UPDATE_RATE)


def main():
    car_state_queue = Queue()
    tls_history = TLSHistory()
    print("starting TLS simulator thread")
    TLSSimulatorThread(tls_history).start()
    print("starting car simulator thread")
    CarSimulatorThread(car_state_queue).start()
    while True:
        car_crossed = car_state_queue.get()
        if car_crossed:
            print("car crossed in %s" % tls_history.get_current_state().name)
            if tls_history.get_current_state() == TLS.R:
                print("transition timestamp: %.1f" % tls_history.get_last_transition_to_red_timestamp())

            exit(0)


if __name__ == "__main__":
    main()
