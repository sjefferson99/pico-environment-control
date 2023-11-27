from time import sleep
from machine import Pin

status_led = Pin("LED", Pin.OUT)

def flash_led(count: int, hz: float) -> None:
    status_led.off()
    sleep_duration = (1 / hz) / 2
    for unused in range(count):
        sleep(sleep_duration)
        status_led.on()
        sleep(sleep_duration)
        status_led.off()