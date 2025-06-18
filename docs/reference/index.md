# Language Reference

This section provides a complete reference for the PROJECT SOVEREIGN programming language.

## Table of Contents

1. [Language Syntax](syntax.md)
2. [Opcodes Reference](opcodes.md)
3. [Data Types](data-types.md)
4. [Memory Model](memory-model.md)
5. [Execution Model](execution-model.md)
6. [Error Handling](error-handling.md)

## Language Overview

PROJECT SOVEREIGN is an assembly-like language with a minimal instruction set designed for clarity and self-modification capabilities.

### Basic Concepts

- **Instructions**: Single operations that manipulate data or control flow
- **Stack-based**: Operations primarily work with values on the stack
- **Dual Stacks**: Separate data and control stacks
- **Memory**: Addressable storage using hexadecimal addresses
- **Registers**: Named storage locations (r0, r1, r2, ...)

### Program Structure

A PROJECT SOVEREIGN program consists of:
- Instructions (one per line)
- Labels (targets for jumps)
- Comments (start with `;`)

```assembly
; This is a comment
main:           ; This is a label
    PUSH #42    ; Push immediate value
    CALL func   ; Call function
    HALT        ; Stop execution
    
func:
    DUP         ; Duplicate top of stack
    RET         ; Return to caller
```

### Operand Types

1. **Immediate Values**: `#42`, `#-10`
2. **Registers**: `r0`, `r1`, `r2`
3. **Memory Addresses**: `@FF00`, `@1234`
4. **Labels**: `loop`, `main`, `error_handler`
5. **String Literals**: `"Hello, World!"`

### Execution Flow

Programs execute sequentially unless altered by control flow operations:
- `JMP` - Unconditional jump
- `JZ`/`JNZ` - Conditional jumps
- `CALL`/`RET` - Function calls
- `HALT` - Stop execution

### Self-Modification

PROJECT SOVEREIGN supports homoiconic design principles:
- Code can be treated as data
- Programs can modify themselves
- LLM integration enables dynamic code generation
- Evolution mechanisms allow self-improvement