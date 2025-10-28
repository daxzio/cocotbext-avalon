.PHONY: help clean dist lint mypy test

help:
	@echo "cocotbext-avalon Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  test       - Run all tests"
	@echo "  lint       - Run pyflakes and ruff linters"
	@echo "  mypy       - Run mypy type checker"
	@echo "  dist       - Build distribution packages"
	@echo "  clean      - Clean build artifacts"
	@echo "  install    - Install package in development mode"

test:
	@echo "Running tests in tests/test_slverr..."
	cd tests/test_slverr && make sim SIM=verilator

lint:
	@echo "Running pyflakes..."
	pyflakes cocotbext/
	@echo "Running ruff..."
	ruff check cocotbext/

mypy:
	@echo "Running mypy type checker..."
	mypy cocotbext/avalon --ignore-missing-imports || true

dist:
	@echo "Building distribution packages..."
	python -m build
	@echo "Checking package..."
	twine check dist/*

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf cocotbext_avalon.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name sim_build -exec rm -rf {} + 2>/dev/null || true
	find . -name results.xml -delete
	find . -name "*.vcd" -delete
	find . -name "*.fst" -delete

install:
	@echo "Installing in development mode..."
	pip install -e .

.DEFAULT_GOAL := help

