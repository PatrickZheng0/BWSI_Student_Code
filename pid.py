import time

class PID:

    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time

        self.clear()

    def update(self, feedback_value, current_time=None):
        error = self.SetPoint - feedback_value
        self.current_time = current_time if current_time is not None else time.time()
        delta_time = self.current_time - self.last_time

        if delta_time >= self.sample_time:
            self.PTerm = error
            self.ITerm += error*delta_time
            if delta_time > 0:
                self.DTerm = (error - self.last_error)/delta_time

            self.last_time = self.current_time
            self.last_error = error

            self.output = (self.Kp * self.PTerm) + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def get_set_point(self):
        return self.SetPoint

    def set_sample_time(self, sample_time):
        self.sample_time = sample_time

    def clear(self):
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        self.output = 0.0