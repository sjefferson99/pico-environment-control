from machine import Pin
import uasyncio
from lib.ulogging import uLogger
from lib.display import Display

class Button:

    def __init__(self, log_level: int, GPIO_pin: int, display: Display) -> None:
        self.log_level = log_level
        self.logger = uLogger(f"Button {GPIO_pin}", log_level)
        self.pin = Pin(GPIO_pin, Pin.IN, Pin.PULL_UP)
        self.button_pressed = uasyncio.Event()
        self.display = display

    async def wait_for_press(self) -> None:
        self.logger.info("Starting button press watcher")
        
        while True:
            previous_value = self.pin.value()
            while (self.pin.value() == previous_value):
                previous_value = self.pin.value()
                await uasyncio.sleep(0.04)
            
            self.logger.info("Button pressed")
            if self.display.backlight_on_time_ms == 0:
                self.logger.info("Enabling backlight - button_pressed not set")
                self.display.backlight_on()
            else:
                self.logger.info("Backlight on - Setting button_pressed")
                self.display.backlight_on() # Reset backlight timeout
                self.button_pressed.set()

    def set_function_on_press(self, function, function_args: list = []) -> None:
        uasyncio.create_task(self.function_on_press(function, function_args))
    
    async def function_on_press(self, function, function_args: list = []) -> None:
        while True:
            await self.button_pressed.wait()
            self.button_pressed.clear()
            function(self, *function_args)

    def test_button_function(self) -> None:
        self.logger.info("Test button function executed")
