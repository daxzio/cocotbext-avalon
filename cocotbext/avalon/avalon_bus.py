"""

Copyright (c) 2024-2025 Daxzio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from typing import List
from cocotb_bus.bus import Bus


class AvalonBus(Bus):
    """Avalon Memory-Mapped (MM) bus signals"""

    _signals = [
        "read",
        "write",
        "waitrequest",
        "address",
        "writedata",
        "byteenable",
        "readdatavalid",
        "writeresponsevalid",
        "readdata",
        "response",
    ]
    _optional_signals: List[str] = []

    def __init__(
        self, entity=None, prefix=None, signals=None, optional_signals=None, **kwargs
    ):
        if signals is None:
            signals = self._signals
        if optional_signals is None:
            optional_signals = self._optional_signals
        super().__init__(
            entity, prefix, signals, optional_signals=optional_signals, **kwargs
        )

    @classmethod
    def from_entity(cls, entity, **kwargs):
        return cls(entity, **kwargs)

    @classmethod
    def from_prefix(cls, entity, prefix, **kwargs):
        return cls(entity, prefix, **kwargs)

