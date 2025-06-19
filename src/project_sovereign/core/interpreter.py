"""
Main interpreter for PROJECT SOVEREIGN.

Coordinates parsing, execution, and error handling.
"""

import logging
from pathlib import Path

from ..vm.virtual_machine import SovereignVM
from .parser import ParseError, SovereignParser


class SovereignInterpreter:
    """
    High-level interpreter for PROJECT SOVEREIGN programs.

    Provides a simple interface for parsing and executing
    assembly programs with integrated error handling.
    """

    def __init__(self):
        self.parser = SovereignParser()
        self.vm = SovereignVM()
        self.logger = logging.getLogger(__name__)

    def run(self, source: str) -> None:
        """
        Parse and execute PROJECT SOVEREIGN source code.

        Args:
            source: Assembly source code to execute

        Raises:
            ParseError: If source code is invalid
            RuntimeError: If execution fails
        """
        # Parse the source code
        try:
            program = self.parser.parse(source)
            self.logger.info(
                f"Successfully parsed program with {len(program.instructions)} instructions"
            )
        except ParseError as e:
            self.logger.error(f"Parse error: {e}")
            raise

        # Execute the program
        try:
            self.vm.execute(program)
            self.logger.info("Program execution completed successfully")
        except Exception as e:
            self.logger.error(f"Runtime error: {e}")
            raise RuntimeError(f"Execution failed: {e}") from e

    def run_file(self, filepath: str | Path) -> None:
        """
        Load and execute a PROJECT SOVEREIGN file.

        Args:
            filepath: Path to the .sov file

        Raises:
            FileNotFoundError: If file doesn't exist
            ParseError: If source code is invalid
            RuntimeError: If execution fails
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        source = filepath.read_text()
        self.run(source)

    def execute_single(self, instruction_str: str) -> None:
        """
        Execute a single instruction (for REPL mode).

        Args:
            instruction_str: Single instruction to execute

        Raises:
            ParseError: If instruction is invalid
            RuntimeError: If execution fails
        """
        try:
            instruction = self.parser.parse_instruction(instruction_str)
            self.vm.execute_instruction(instruction)
        except Exception as e:
            self.logger.error(f"Failed to execute instruction: {e}")
            raise

    def get_vm_state(self) -> dict:
        """Get current VM state for debugging."""
        return self.vm.dump_state()

    def reset(self) -> None:
        """Reset interpreter to initial state."""
        self.vm.reset()
        self.logger.info("Interpreter reset to initial state")
