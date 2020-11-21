from threading import Event

class event:
    def __init__(self):
        self.event = Event()

    def sleep(self,seconds = None):
        self.event.clear()
        time_out = self.event.wait(timeout=seconds)
        return time_out

    def wake_up(self):
        self.event.set()