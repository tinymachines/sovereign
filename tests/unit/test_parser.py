"""
Tests for PROJECT SOVEREIGN parser.
"""

import pytest
from project_sovereign.core.parser import SovereignParser, ParseError
from project_sovereign.core.ast_nodes import Program, Instruction, Register, Immediate


class TestSovereignParser:
    """Test cases for the parser."""

    def test_parse_simple_instruction(self, parser):
        """Test parsing a simple instruction."""
        source = "PUSH #42"
        program = parser.parse(source)

        assert len(program.instructions) == 1
        instruction = program.instructions[0]
        assert instruction.opcode == "PUSH"
        assert len(instruction.operands) == 1
        assert isinstance(instruction.operands[0], Immediate)
        assert instruction.operands[0].value == 42

    def test_parse_multiple_instructions(self, parser):
        """Test parsing multiple instructions."""
        source = """
        PUSH #10
        PUSH #20
        ADD
        """
        program = parser.parse(source)

        assert len(program.instructions) == 3
        assert program.instructions[0].opcode == "PUSH"
        assert program.instructions[1].opcode == "PUSH"
        assert program.instructions[2].opcode == "ADD"

    def test_parse_with_labels(self, parser):
        """Test parsing with labels."""
        source = """
        loop:
        PUSH #1
        JMP loop
        """
        program = parser.parse(source)

        assert "loop" in program.labels
        assert program.labels["loop"] == 0

    def test_parse_registers(self, parser):
        """Test parsing register operands."""
        source = "LOAD r5"
        program = parser.parse(source)

        operand = program.instructions[0].operands[0]
        assert isinstance(operand, Register)
        assert operand.number == 5

    def test_invalid_syntax_raises_error(self, parser):
        """Test that invalid syntax raises ParseError."""
        with pytest.raises(ParseError):
            parser.parse("INVALID SYNTAX $$")

    def test_validate_syntax(self, parser):
        """Test syntax validation."""
        valid_source = "PUSH #42\nHALT"
        invalid_source = "INVALID $$"

        assert parser.validate_syntax(valid_source) is True
        assert parser.validate_syntax(invalid_source) is False


@pytest.mark.parametrize(
    "source,expected_opcodes",
    [
        ("PUSH #1\nPOP", ["PUSH", "POP"]),
        ("ADD\nSUB\nMUL", ["ADD", "SUB", "MUL"]),
        ("JMP loop\nloop:\nHALT", ["JMP", "HALT"]),
    ],
)
def test_parse_instruction_types(parser, source, expected_opcodes):
    """Parametrized test for different instruction types."""
    program = parser.parse(source)
    actual_opcodes = [inst.opcode for inst in program.instructions]
    assert actual_opcodes == expected_opcodes
