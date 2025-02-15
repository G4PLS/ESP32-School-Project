import machine
import neopixel

class LedMatrix:
    def __init__(self, pin, rows, columns):
        self._pin = machine.Pin(pin, machine.Pin.OUT)

        self.led_matrix = neopixel.NeoPixel(self._pin, rows*columns)
        self.rows = rows
        self.columns = columns
        self.total_leds = rows * columns

    def set_color(self, row, column, color: tuple[int,int,int]):
        if not (0 <= row <= self.rows):
            raise ValueError(f"Row index {row} out of bounds. Must be between 0 and {self.rows - 1}.")
        if  not (0 <= column <= self.columns):
            raise ValueError(f"Column index {column} out of bounds. Must be between 0 and {self.columns - 1}.")

        index = row * self.columns + column

        if index >= self.total_leds:
            raise ValueError(f"Index {index} out of bounds. Must be between 0 and {self.total_leds - 1}.")

        self.led_matrix[index] = list(color)
        self.led_matrix.write()

    def on(self, color: tuple[int,int,int]=(255,255,255)):
        for x in range(self.rows):
            for y in range(self.columns):
                self.set_color(x,y,color)
    
    def off(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.set_color(x,y, (0,0,0))