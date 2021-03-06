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

from Midi.ProgramChange import ProgramChangeMessage
from Midi.MidiInterface import MidiInterface
from Button.PushButton import PushButton

def main():
    interface = MidiInterface()
    prog_changes = [
        ProgramChangeMessage(channel=1, program_number=0),
        ProgramChangeMessage(channel=1, program_number=1)
    ]
    btn_one = PushButton(1, active=PushButton.ACTIVE_HIGH)
    idx = 0

    while True:
        if btn_one.did_release:
            interface.send(prog_changes[idx])

            idx += 1

            if idx >= len(prog_changes):
                idx = 0




if __name__ == "__main__":
    main()