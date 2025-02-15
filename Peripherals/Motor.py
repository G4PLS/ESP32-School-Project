import machine

class Motor:
    CW = 0
    CCW = 1

    def __init__(self, pin_cw, pin_ccw, frequency=1000):
        self._pin_cw = machine.Pin(pin_cw, machine.Pin.OUT)
        self._pin_cw = machine.Pin(pin_ccw, machine.Pin.OUT)

        self.pwm_cw = machine.PWM(self._pin_cw, freq=frequency)
        self.pwm_ccw = machine.PWM(self._pin_ccw, freq=frequency)

        self.current_direction = Motor.CW
        self.current_duty_cycle = 0

    def _apply_duty_cycle(self):
        if not (0 <= self.current_duty_cycle <= 1023):
            raise ValueError("Duty Cycle must be between 0 and 1023")

        if self.current_direction == Motor.CW:
            self.pwm_cw.duty(self.current_duty_cycle)
            self.pwm_ccw.duty(0)
        else:
            self.pwm_cw.duty(0)
            self.pwm_ccw.duty(self.current_duty_cycle)

    def set_direction(self, direction):
        self.current_direction = direction
        self._apply_duty_cycle(self.current_duty_cycle)

    def set_speed_rmp(self, min_rpm, max_rpm, target_rpm):
        duty_cycle_percent = (min_rpm/max_rpm)*target_rpm
        duty_cycle = int(duty_cycle_percent / 100 * 1023)

        self.current_duty_cycle = duty_cycle
        self._apply_duty_cycle()

    def set_speed_cycle(self, duty_cycle):
        self.current_duty_cycle = duty_cycle
        self._apply_duty_cycle()