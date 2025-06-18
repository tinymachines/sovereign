"""
Parser implementation for PROJECT SOVEREIGN assembly syntax.

Uses Lark for grammar definition and parsing of assembly programs
into abstract syntax trees.
"""

from lark import Lark, Transformer, Token
from typing import List, Optional, Union, Any
from dataclasses import dataclass

from .ast_nodes import (
    Program,
    Instruction,
    Label,
    Operand,
    Register,
    Immediate,
    Address,
    StringLiteral,
    LabelRef,
)


# Grammar definition for PROJECT SOVEREIGN assembly
SOVEREIGN_GRAMMAR = """
    start: program

    program: statement*

    statement: instruction 
             | label
    
    instruction: opcode operand*
    
    opcode: WORD
    
    operand: register 
           | immediate 
           | address
           | string_literal
           | label_ref
    
    register: "r" NUMBER
    immediate: "#" SIGNED_NUMBER
    address: "@" HEX_STRING
    string_literal: ESCAPED_STRING
    label_ref: WORD
    
    label: WORD ":"
    
    WORD: /[A-Za-z_][A-Za-z0-9_]*/
    HEX_STRING: /[a-fA-F0-9]+/
    
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.NUMBER
    %import common.WS
    %import common.NEWLINE
    %ignore WS
    %ignore NEWLINE
    %ignore /;[^\\n]*/
"""


class SovereignTransformer(Transformer):
    """Transform parse tree into AST nodes."""

    def program(self, items):
        """Transform program node."""
        instructions = []
        labels = {}

        for item in items:
            if isinstance(item, Instruction):
                instructions.append(item)
            elif isinstance(item, Label):
                labels[item.name] = len(instructions)

        return Program(instructions=instructions, labels=labels)
    
    def statement(self, items):
        """Transform statement node."""
        return items[0]  # Return the instruction or label

    def instruction(self, items):
        """Transform instruction node."""
        opcode = str(items[0])
        operands = items[1:] if len(items) > 1 else []
        # Ensure operands are properly transformed
        transformed_operands = []
        for operand in operands:
            if hasattr(operand, 'children') and operand.children:
                transformed_operands.append(operand.children[0])
            else:
                transformed_operands.append(operand)
        return Instruction(opcode=opcode, operands=transformed_operands)

    def opcode(self, items):
        """Transform opcode token."""
        return str(items[0])

    def register(self, items):
        """Transform register operand."""
        reg_num = int(str(items[0]))  # First item is the number after 'r'
        return Register(number=reg_num)

    def immediate(self, items):
        """Transform immediate operand."""
        value = int(str(items[0]))  # First item is the number after '#'
        return Immediate(value=value)

    def address(self, items):
        """Transform address operand."""
        addr = str(items[0])  # First item is the hex string after '@'
        return Address(value=addr)

    def string_literal(self, items):
        """Transform string literal."""
        # Lark already handles escaped strings
        return StringLiteral(value=str(items[0])[1:-1])  # Remove quotes

    def label_ref(self, items):
        """Transform label reference."""
        return LabelRef(name=str(items[0]))

    def label(self, items):
        """Transform label definition."""
        return Label(name=str(items[0]))


class SovereignParser:
    """
    Parser for PROJECT SOVEREIGN assembly language.

    Converts assembly source code into abstract syntax trees
    for execution by the virtual machine.
    """

    def __init__(self):
        self.parser = Lark(SOVEREIGN_GRAMMAR, parser="lalr")
        self.transformer = SovereignTransformer()

    def parse(self, source: str) -> Program:
        """
        Parse source code into program AST.

        Args:
            source: Assembly source code

        Returns:
            Program AST ready for execution

        Raises:
            ParseError: If source code is invalid
        """
        try:
            parse_tree = self.parser.parse(source)
            result = self.transformer.transform(parse_tree)
            # Extract the Program from the result tree
            if hasattr(result, 'children') and result.children:
                return result.children[0]
            return result
        except Exception as e:
            raise ParseError(f"Failed to parse source: {e}") from e

    def parse_instruction(self, source: str) -> Instruction:
        """Parse a single instruction."""
        # Create a temporary grammar for single instruction
        instruction_grammar = """
            start: instruction
            
            instruction: opcode operand*
            
            opcode: /[A-Z][A-Z0-9]*/
            
            operand: register 
                   | immediate 
                   | address
                   | string_literal
                   | label_ref
            
            register: /r[0-9]+/
            immediate: /#-?[0-9]+/
            address: /@[a-fA-F0-9]+/
            string_literal: ESCAPED_STRING
            label_ref: /[a-z_][a-z0-9_]*/
            
            %import common.ESCAPED_STRING
            %import common.WS
            %ignore WS
        """

        try:
            parser = Lark(instruction_grammar, parser="lalr")
            parse_tree = parser.parse(source)

            # Transform manually for single instruction
            items = parse_tree.children
            opcode = str(items[0].children[0])
            operands = []

            for item in items[0].children[1:]:
                if item.data == "register":
                    reg_num = int(str(item.children[0])[1:])
                    operands.append(Register(number=reg_num))
                elif item.data == "immediate":
                    value = int(str(item.children[0])[1:])
                    operands.append(Immediate(value=value))
                elif item.data == "address":
                    addr = str(item.children[0])[1:]
                    operands.append(Address(value=addr))
                elif item.data == "string_literal":
                    value = str(item.children[0])[1:-1]
                    operands.append(StringLiteral(value=value))
                elif item.data == "label_ref":
                    operands.append(LabelRef(name=str(item.children[0])))

            return Instruction(opcode=opcode, operands=operands)

        except Exception as e:
            raise ParseError(f"Failed to parse instruction: {e}") from e

    def validate_syntax(self, source: str) -> bool:
        """Validate syntax without creating AST."""
        try:
            self.parser.parse(source)
            return True
        except Exception:
            return False


class ParseError(Exception):
    """Exception raised for parsing errors."""

    pass
