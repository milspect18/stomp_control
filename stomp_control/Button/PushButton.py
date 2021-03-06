"""
MIT License

Copyright (c) 2021 PriceTec Designs LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
from machine import Pin, disable_irq, enable_irq

if sys.platform == "rp2":
    IO_NUMS = [io_num for io_num in range(29) if io_num not in [23, 24, 25]]
else:
    IO_NUMS = []

class PushButton:
    """
    Represent a pushbutton switch
    """

    ACTIVE_HIGH = 1
    ACTIVE_LOW = 0

    RELEASED = 0
    PRESSED = 1

    def __init__(self, input_num: int, active: int = ACTIVE_HIGH, max_event: int = 100) -> None:
        self.pin_num = input_num
        self.max_event_count = abs(max_event)
        self._active = active
        self._press_count = 0
        self._release_count = 0

        self._pin = Pin(self.pin_num, mode=Pin.IN, pull=Pin.PULL_DOWN if active else Pin.PULL_UP)
        self._pin.irq(handler=self._edge_detect, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

        self._is_pressed = self._pin.value() == self._active

    @property
    def pin_num(self) -> int:
        return self._pin_num

    @pin_num.setter
    def pin_num(self, new_pin_num) -> None:
        if new_pin_num not in IO_NUMS:
            raise ValueError(f"Invalid pin number.  Valid IO pin numbers: {IO_NUMS}")

        self._pin_num = new_pin_num

    @property
    def state(self) -> int:
        state = disable_irq()
        val = self.PRESSED if self._is_pressed else self.RELEASED
        enable_irq(state)
        return val

    @property
    def did_press(self) -> bool:
        state = disable_irq()
        _did_press = self._press_count > 0
        self._press_count = max(0, self._press_count - 1)
        enable_irq(state)

        return _did_press

    @property
    def did_release(self) -> bool:
        state = disable_irq()
        _did_release = self._release_count > 0
        self._release_count = max(0, self._release_count - 1)
        enable_irq(state)

        return _did_release

    def clear_press_events(self):
        state = disable_irq()
        self._press_count = 0
        enable_irq(state)

    def clear_release_events(self):
        state = disable_irq()
        self._release_count = 0
        enable_irq(state)

    def clear_all_events(self):
        self.clear_press_events()
        self.clear_release_events()

    def _edge_detect(self, pin: Pin) -> None:
        self._is_pressed = self._active == pin.value()

        if self._is_pressed and self._press_count < self.max_event_count:
            self._press_count += 1
        elif not self._is_pressed and self._release_count < self.max_event_count:
            self._release_count += 1


