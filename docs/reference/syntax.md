# Language Syntax

PROJECT SOVEREIGN uses a simple, assembly-like syntax designed for clarity and ease of parsing.

## Basic Syntax Rules

### Instructions
- One instruction per line
- Opcode followed by zero or more operands
- Opcodes are case-insensitive (convention: uppercase)
- Operands are separated by spaces

```assembly
PUSH #42
ADD
STORE @result
HALT
```

### Comments
- Comments start with semicolon (`;`)
- Can appear on their own line or after instructions
- Everything after `;` is ignored

```assembly
; This is a full-line comment
PUSH #42    ; This is an inline comment
```

### Labels
- Labels end with colon (`:`)
- Must start with letter or underscore
- Can contain letters, numbers, underscores
- Case-sensitive

```assembly
main:
    PUSH #1
    
loop_start:
    DUP
    JNZ loop_start
```

## Operand Types

### Immediate Values
- Prefix: `#`
- Decimal integers (positive or negative)
- Examples: `#42`, `#-10`, `#0`

```assembly
PUSH #42       ; Push 42 onto stack
PUSH #-100     ; Push -100 onto stack
```

### Registers
- Prefix: `r`
- Followed by register number
- Examples: `r0`, `r1`, `r15`

```assembly
PUSH r0        ; Push value from register 0
STORE r1       ; Store to register 1
```

### Memory Addresses
- Prefix: `@`
- Hexadecimal address
- Examples: `@FF00`, `@1234`, `@DEAD`

```assembly
LOAD @1000     ; Load from memory address 0x1000
STORE @BEEF    ; Store to memory address 0xBEEF
```

### Labels References
- No prefix
- Used for jumps and calls
- Must match a defined label

```assembly
JMP start      ; Jump to 'start' label
CALL function  ; Call 'function' label
```

### String Literals
- Enclosed in double quotes
- Supports escape sequences
- Used with IO operations

```assembly
FOPEN "data.txt"
LLMGEN "generate a sort function"
```

## Program Structure

### Basic Program Layout
```assembly
; Program header comment
; Author: Your Name
; Description: What this program does

; Constants and data
PUSH #100
STORE @max_value

; Main program
main:
    LOAD @max_value
    CALL process
    HALT

; Functions
process:
    DUP
    PUSH #2
    DIV
    RET

; Error handlers
error:
    PUSH #-1
    HALT
```

### Function Convention
```assembly
; Function: multiply
; Input: Two values on stack [a, b]
; Output: Product on stack [a*b]
multiply:
    MUL
    RET

; Usage:
PUSH #6
PUSH #7
CALL multiply
; Stack now contains [42]
```

## Style Guidelines

### Naming Conventions
- **Labels**: `snake_case` for functions and labels
- **Constants**: Store at known addresses with descriptive names
- **Comments**: Explain why, not what

### Indentation
- No indentation for labels
- 4 spaces for instructions
- Align operands for readability

```assembly
main:
    PUSH  #10
    PUSH  #20
    ADD
    STORE @result
    HALT
```

### Organization
1. File header with description
2. Constants and initialization
3. Main program logic
4. Function definitions
5. Error handlers

## Common Patterns

### Loop Structure
```assembly
    PUSH #10          ; Counter
loop:
    DUP              ; Duplicate counter
    JZ   end_loop    ; Exit if zero
    
    ; Loop body here
    
    PUSH #1
    SUB              ; Decrement counter
    JMP  loop
end_loop:
    DROP             ; Clean up counter
```

### Conditional Execution
```assembly
    PUSH #42
    PUSH #42
    SUB              ; Compare values
    JZ   equal       ; Jump if equal
    
    ; Not equal case
    PUSH #0
    JMP  done
    
equal:
    PUSH #1
    
done:
    ; Continue...
```

### Stack Manipulation
```assembly
; Save and restore value
    DUP              ; Save copy
    CALL process     ; May modify stack
    SWAP             ; Restore original
    DROP             ; Remove processed
```

## Error Handling

### Stack Underflow Protection
```assembly
safe_pop:
    ; Check if stack has value
    PUSH #0
    OVER
    JZ   stack_empty
    
    ; Safe to pop
    SWAP
    DROP
    RET
    
stack_empty:
    PUSH #-1     ; Error code
    RET
```

### Division by Zero Check
```assembly
safe_divide:
    DUP          ; Check divisor
    JZ   div_zero
    DIV
    RET
    
div_zero:
    DROP         ; Remove divisor
    DROP         ; Remove dividend
    PUSH #0      ; Return 0 or error
    RET
```