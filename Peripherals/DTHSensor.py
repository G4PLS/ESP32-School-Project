import machine
import dht

class DHT:
    def __init__(self, pin):
        self._pin = machine.pin(pin)
        self.dht = dht.DHT11(self._pin)

    def measure(self):
        self.dht.measure()
        return self.dht.temperature(), self.dht.humidity()
    
    def temperature(self):
        return self.dht.temperature()
    
    def humidity(self):
        return self.dht.humidity()