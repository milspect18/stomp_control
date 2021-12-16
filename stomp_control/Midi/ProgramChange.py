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

from Midi.Status import StatusMessage


class ProgramChangeMessage(StatusMessage):
    """
    Format a program change message
    """

    def __init__(self, channel: int, program_number: int) -> None:
        self.channel = channel
        self.program_number = program_number

    @property
    def serialized(self) -> bytes:
        if self.channel is None or self.program_number is None:
            return bytes()

        return bytes([self._status_byte(), self.program_number])

    @property
    def channel(self) -> int:
        return self._chn_num

    @channel.setter
    def channel(self, channel_num: int) -> None:
        if channel_num < 0 or channel_num > 15:
            raise ValueError("Channel number must be between 0 and 15")

        self._chn_num = channel_num

    @property
    def program_number(self) -> int:
        return self._prog_num

    @program_number.setter
    def program_number(self, prog_num: int) -> None:
        if prog_num < 0 or prog_num > 127:
            raise ValueError("Program number must be between 0 and 127")

        self._prog_num = prog_num

    def _status_byte(self) -> int:
        chn = self.channel if self.channel else 0

        return (self.PROGRAM_CHANGE << 4) | chn
