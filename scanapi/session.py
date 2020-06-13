from datetime import datetime


class Session:
    def __init__(self):
        self.successes = 0
        self.failures = 0

    def start(self):
        self.started_at = datetime.now()

    def increment_successes(self):
        self.successes += 1

    def increment_failures(self):
        self.failures += 1

    def elapsed_time(self):
        return datetime.now() - self.started_at


session = Session()
