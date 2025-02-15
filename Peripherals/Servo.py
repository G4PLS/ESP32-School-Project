import machine
from time import sleep

class Servo:
    def __init__(self, pin, start_angle=0, frequency=50):
        self._pin = machine.Pin(pin, machine.Pin.OUT)
        self.pwm = machine.PWM(self._pin, freq=frequency)
        
        self.current_angle = start_angle
        self.start_angle = start_angle
        self.move_to(start_angle)

    @staticmethod
    def angle_to_duty(angle, base_percent=5):
        duty_cycle_percent = base_percent + (angle/180) * 10
        return int(duty_cycle_percent / 100 * 1023)
    
    def move_to(self, angle):
        duty_cycle = Servo.angle_to_duty(angle)
        self.pwm.duty(duty_cycle)
        self.current_angle = angle

    def move_smoothly(self, target_angle, smoothness=10, duration=1):
        """
        duration in s
        """
        angle_difference = target_angle - self.current_angle

        step_size = angle_difference / smoothness

        total_time = abs(angle_difference) / duration
        time_per_step = total_time / smoothness

        for i in range(smoothness):
            self.move_to(self.current_angle + step_size)
            sleep(time_per_step)

        self.current_angle = target_angle

    def reset(self):
        self.move_to(self.start_angle)