# Avalon-MM interface modules for Cocotb

GitHub repository: https://github.com/daxzio/cocotbext-avalon

## Introduction

Avalon Memory-Mapped (MM) simulation models for [cocotb](https://github.com/cocotb/cocotb).

The Avalon-MM protocol is defined by Intel/Altera for use in FPGA and ASIC designs, particularly with Platform Designer (Qsys).

## Features

- **AvalonMaster**: Manager/Master driver for Avalon-MM protocol
- **AvalonBus**: Bus signal container with auto-discovery
- **Wide data support**: Automatically splits data wider than bus into multiple transactions
- **Word addressing**: Properly handles word-based addressing
- **Error handling**: Full error response validation with exception control
- **Timeout support**: Configurable transaction timeouts
- **Setup time**: Proper timing for combinational request logic

## Installation

Installation from pip (when available):

    $ pip install cocotbext-avalon

Installation from git (latest development version):

    $ pip install https://github.com/daxzio/cocotbext-avalon/archive/main.zip

Installation for active development:

    $ git clone https://github.com/daxzio/cocotbext-avalon
    $ pip install -e cocotbext-avalon

## Avalon-MM Protocol Overview

Avalon-MM uses a request/response protocol with **word addressing**:

**Request Phase:**
- Separate `read` and `write` control signals
- `waitrequest` signal provides back-pressure
- **Word addressing** (address × bytes_per_word = byte offset)
- Byte enables for partial word writes

**Response Phase:**
- `readdatavalid` indicates valid read data
- `writeresponsevalid` indicates write completion
- 2-bit `response` signal for error reporting (0x0=OK, 0x2=SLVERR)

## Usage Example

### Avalon Bus

The `AvalonBus` is used to map to an Avalon-MM interface on the `dut`.

#### Required Signals:
* _read_ - Read request
* _write_ - Write request
* _waitrequest_ - Back-pressure/stall
* _address_ - Word address (not byte!)
* _writedata_ - Write data
* _byteenable_ - Byte enable
* _readdatavalid_ - Read data valid
* _writeresponsevalid_ - Write response valid
* _readdata_ - Read data
* _response_ - Response code (2-bit)

### Avalon Master

The `AvalonMaster` class implements an Avalon-MM manager/master.

The master automatically handles data wider than the bus width by splitting transactions into multiple sequential Avalon accesses at consecutive addresses.

```python
from cocotbext.avalon import AvalonMaster, AvalonBus

bus = AvalonBus.from_prefix(dut, "avalon")
avalon_driver = AvalonMaster(bus, dut.clk)
```

Once instantiated, read and write operations can be initiated:

```python
# Write operations
await avalon_driver.write(0x1000, 0x12345678)  # Single 32-bit write
await avalon_driver.write(0x2000, 0x123456789ABCDEF0)  # Auto-splits to two writes

# Read operations
data = await avalon_driver.read(0x1000)  # Returns bytes
value = int.from_bytes(data, 'little')

# With data verification
await avalon_driver.read(0x1000, 0x12345678)  # Raises exception if mismatch

# With error expectation
await avalon_driver.write(0xBAD_ADDR, 0xFF, error_expected=True)
```

#### Important: Word Addressing

**Avalon-MM uses WORD addressing, not byte addressing!**

For 32-bit data (4 bytes per word):
- Word address 0x00 = Byte address 0x00
- Word address 0x01 = Byte address 0x04
- Word address 0x10 = Byte address 0x40

The driver handles this conversion automatically - you provide byte addresses.

#### `AvalonMaster` Constructor Parameters
* _bus_: `AvalonBus` object containing Avalon-MM interface signals
* _clock_: Clock signal
* _timeout_cycles_: Maximum clock cycles to wait before timing out (optional, default `1000`). Set to `-1` to disable timeout.

#### Methods
* `wait()`: Blocking wait until all outstanding operations complete
* `write(addr, data, strb=-1, error_expected=False)`: Write _data_ (bytes or int) to _addr_, wait for result. Auto-splits wide data.
* `write_nowait(addr, data, strb=-1, error_expected=False)`: Write _data_ to _addr_, queue without waiting.
* `read(addr, data=bytes(), error_expected=False)`: Read bytes at _addr_. Auto-splits wide data.
* `read_nowait(addr, data=bytes(), error_expected=False)`: Read bytes at _addr_, queue without waiting.

#### Error Handling

```python
# Normal operation - exceptions enabled
await avalon.write(read_only_addr, data, error_expected=True)  # OK

# For testing error detection without exceptions
avalon.exception_enabled = False
await avalon.write(read_only_addr, data, error_expected=False)
assert avalon.exception_occurred == True  # Error was detected
```

## Complete Example

```python
import cocotb
from cocotb.triggers import RisingEdge
from cocotbext.avalon import AvalonBus, AvalonMaster

@cocotb.test()
async def test_avalon(dut):
    # Create Avalon master
    avalon_bus = AvalonBus.from_prefix(dut, "avalon")
    avalon_master = AvalonMaster(avalon_bus, dut.clk)
    
    # Reset
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    
    # Write some data
    await avalon_master.write(0x00, 0x12345678)
    await avalon_master.write(0x04, 0xABCDEF00)
    
    # Read back and verify
    await avalon_master.read(0x00, 0x12345678)
    await avalon_master.read(0x04, 0xABCDEF00)
    
    # Test 64-bit access on 32-bit bus (auto-splits)
    await avalon_master.write(0x100, 0x123456789ABCDEF0)
    await avalon_master.read(0x100, 0x123456789ABCDEF0)
```

## Testing

### Package Tests

```bash
cd tests/test_slverr
make sim SIM=verilator
```

**Test Results:** ✅ 3/3 PASS (Verilator and Icarus)

### Integration Tests

See the PeakRDL-etana `tests/` directory for comprehensive testbenches using cocotbext-avalon across 30+ test scenarios.

## License

MIT License. See LICENSE file for details.

## References

- [Intel Avalon Interface Specifications](https://www.intel.com/content/www/us/en/docs/programmable/683091/current/introduction-to-the-interface-specifications.html)
- [Cocotb Documentation](https://docs.cocotb.org/)
- [PeakRDL-etana](https://github.com/daxzio/PeakRDL-etana) - Uses this package for Avalon-MM testing

