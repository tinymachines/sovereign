"""
Pytest configuration and fixtures for PROJECT SOVEREIGN tests.
"""

from pathlib import Path

import pytest

from project_sovereign.core.interpreter import SovereignInterpreter
from project_sovereign.core.opcodes import OpCodeRegistry
from project_sovereign.core.parser import SovereignParser
from project_sovereign.vm.virtual_machine import SovereignVM


@pytest.fixture
def parser():
    """Provide parser instance for tests."""
    return SovereignParser()


@pytest.fixture
def vm():
    """Provide VM instance for tests."""
    return SovereignVM()


@pytest.fixture
def interpreter():
    """Provide interpreter instance for tests."""
    return SovereignInterpreter()


@pytest.fixture
def opcode_registry():
    """Provide opcode registry for tests."""
    return OpCodeRegistry()


@pytest.fixture
def sample_program():
    """Provide sample program for testing."""
    return """
    ; Simple test program
    PUSH #42
    PUSH #10
    ADD
    POP
    HALT
    """


@pytest.fixture
def test_data_dir():
    """Provide test data directory."""
    return Path(__file__).parent / "data"
