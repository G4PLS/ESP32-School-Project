import machine

class Sensor:
    def __init__(self, pin, pull=None):
        self._pin = machine.Pin(pin, machine.Pin.IN, pull)

    def get_state(self):
        return self._pin.value()