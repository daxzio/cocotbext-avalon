# Contributing to cocotbext-avalon

Thank you for your interest in contributing to cocotbext-avalon!

## Development Setup

### Clone and Install

```bash
git clone https://github.com/daxzio/cocotbext-avalon.git
cd cocotbext-avalon
pip install -e .
pip install pytest flake8 mypy
```

### Install Dependencies

```bash
pip install -r requirements.txt
pip install peakrdl-etana  # For RTL generation in tests
```

### Install Simulators

**Verilator:**
```bash
# Ubuntu/Debian
sudo apt-get install verilator

# Or use setup-verilator action for latest version
```

**Icarus Verilog:**
```bash
sudo apt-get install iverilog
```

## Running Tests

### Run All Tests

```bash
make test
```

### Run Specific Test

```bash
cd tests/test_slverr
make etana          # Generate RTL
make sim SIM=verilator
make sim SIM=icarus
```

## Code Quality

### Linting

```bash
make lint
```

### Type Checking

```bash
make mypy
```

## Adding New Features

### Adding a New Test

1. Create test directory under `tests/`
2. Add RDL file, test_dut.py, and Makefile
3. Update CI workflows if needed
4. Document the test

### Adding New Functionality

1. Add implementation to appropriate module in `cocotbext/obi/`
2. Add tests
3. Update README.md with examples
4. Update version in `version.py` (follow semver)

## Submitting Changes

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make test lint`)
5. Commit your changes with clear messages
6. Push to your fork
7. Open a Pull Request

### Commit Message Guidelines

Use clear, descriptive commit messages:

```
Add ObiSlave implementation

- Implements subordinate/slave side of Avalon-MM protocol
- Supports memory-mapped responses
- Includes tests for basic operation
```

## Code Style

- Follow PEP 8 guidelines
- Maximum line length: 119 characters
- Use type hints where appropriate
- Document public APIs with docstrings

## Testing Standards

- All new features must include tests
- Maintain 100% pass rate on existing tests
- Test with both Verilator and Icarus
- Add integration tests if appropriate

## Questions?

Open an issue on GitHub or contact the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

