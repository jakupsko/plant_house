import machine
import utime

class Rotary:
    ROT_CW = 1
    ROT_CCW = 2
    SW_PRESS = 4
    SW_RELEASE = 8

    def __init__(self, dt, clk, sw):
        self.dt_pin = machine.Pin(dt, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.clk_pin = machine.Pin(clk, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.sw_pin = machine.Pin(sw, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.last_status = (self.dt_pin.value() << 1) | self.clk_pin.value()

        # Set up interrupts for rotary movement and switch press
        self.dt_pin.irq(handler=self.rotary_change, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.clk_pin.irq(handler=self.rotary_change, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.sw_pin.irq(handler=self.switch_detect, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)

        self.handlers = []
        self.last_button_status = self.sw_pin.value()

    def rotary_change(self, pin):
        new_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        if new_status == self.last_status:
            return

        transition = (self.last_status << 2) | new_status
        if transition == 0b1110:
            self.call_handlers(Rotary.ROT_CW)
        elif transition == 0b1101:
            self.call_handlers(Rotary.ROT_CCW)

        self.last_status = new_status

    def switch_detect(self, pin):
        if self.last_button_status == self.sw_pin.value():
            return

        self.last_button_status = self.sw_pin.value()
        if self.sw_pin.value():
            self.call_handlers(Rotary.SW_RELEASE)
        else:
            self.call_handlers(Rotary.SW_PRESS)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def call_handlers(self, event_type):
        for handler in self.handlers:
            handler(event_type)

# Example usage:
def handle_rotary_event(event_type):
    if event_type == Rotary.ROT_CW:
        print("Rotary clockwise")
    elif event_type == Rotary.ROT_CCW:
        print("Rotary counterclockwise")
    elif event_type == Rotary.SW_PRESS:
        print("Switch pressed")
    elif event_type == Rotary.SW_RELEASE:
        print("Switch released")

if __name__ == '__main__':
    # Create a rotary encoder instance
    my_rotary = Rotary(dt=12, clk=11, sw=13)
    my_rotary.add_handler(handle_rotary_event)

    print("Rotary encoder example. Rotate the encoder or press the switch!")

    # Keep the program running
    while True:
        utime.sleep(100)
