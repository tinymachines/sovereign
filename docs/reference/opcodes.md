# Opcodes Reference

PROJECT SOVEREIGN provides exactly 32 operations organized into 4 categories.

## Stack Operations (8)

### PUSH
**Syntax**: `PUSH value`  
**Description**: Push a value onto the data stack  
**Example**: `PUSH #42`, `PUSH r0`, `PUSH @1000`

### POP
**Syntax**: `POP`  
**Description**: Remove and discard the top value from the data stack  
**Example**: `POP`

### DUP
**Syntax**: `DUP`  
**Description**: Duplicate the top value on the data stack  
**Stack**: `[a] → [a, a]`  
**Example**: `DUP`

### SWAP
**Syntax**: `SWAP`  
**Description**: Exchange the top two values on the data stack  
**Stack**: `[a, b] → [b, a]`  
**Example**: `SWAP`

### ROT
**Syntax**: `ROT`  
**Description**: Rotate the top three values on the data stack  
**Stack**: `[a, b, c] → [b, c, a]`  
**Example**: `ROT`

### OVER
**Syntax**: `OVER`  
**Description**: Copy the second value over the top  
**Stack**: `[a, b] → [a, b, a]`  
**Example**: `OVER`

### DROP
**Syntax**: `DROP`  
**Description**: Remove the top value without returning it  
**Stack**: `[a] → []`  
**Example**: `DROP`

### CLEAR
**Syntax**: `CLEAR`  
**Description**: Remove all values from the data stack  
**Stack**: `[...] → []`  
**Example**: `CLEAR`

## Arithmetic/Logic Operations (8)

### ADD
**Syntax**: `ADD`  
**Description**: Add top two values  
**Stack**: `[a, b] → [a + b]`  
**Example**: `PUSH #10` / `PUSH #32` / `ADD` (result: 42)

### SUB
**Syntax**: `SUB`  
**Description**: Subtract top from second  
**Stack**: `[a, b] → [a - b]`  
**Example**: `PUSH #50` / `PUSH #8` / `SUB` (result: 42)

### MUL
**Syntax**: `MUL`  
**Description**: Multiply top two values  
**Stack**: `[a, b] → [a * b]`  
**Example**: `PUSH #6` / `PUSH #7` / `MUL` (result: 42)

### DIV
**Syntax**: `DIV`  
**Description**: Integer division of second by top  
**Stack**: `[a, b] → [a / b]`  
**Example**: `PUSH #84` / `PUSH #2` / `DIV` (result: 42)

### AND
**Syntax**: `AND`  
**Description**: Bitwise AND of top two values  
**Stack**: `[a, b] → [a & b]`  
**Example**: `PUSH #63` / `PUSH #42` / `AND` (result: 42)

### OR
**Syntax**: `OR`  
**Description**: Bitwise OR of top two values  
**Stack**: `[a, b] → [a | b]`  
**Example**: `PUSH #40` / `PUSH #2` / `OR` (result: 42)

### XOR
**Syntax**: `XOR`  
**Description**: Bitwise XOR of top two values  
**Stack**: `[a, b] → [a ^ b]`  
**Example**: `PUSH #50` / `PUSH #24` / `XOR` (result: 42)

### NOT
**Syntax**: `NOT`  
**Description**: Bitwise NOT of top value  
**Stack**: `[a] → [~a]`  
**Example**: `PUSH #-43` / `NOT` (result: 42)

## Control Flow Operations (8)

### JMP
**Syntax**: `JMP label`  
**Description**: Unconditional jump to label  
**Example**: `JMP main`

### JZ
**Syntax**: `JZ label`  
**Description**: Jump if top of stack is zero  
**Example**: `PUSH #0` / `JZ zero_handler`

### JNZ
**Syntax**: `JNZ label`  
**Description**: Jump if top of stack is not zero  
**Example**: `PUSH #1` / `JNZ continue`

### CALL
**Syntax**: `CALL label`  
**Description**: Call function at label (pushes return address)  
**Example**: `CALL process_data`

### RET
**Syntax**: `RET`  
**Description**: Return from function call  
**Example**: `RET`

### FORK
**Syntax**: `FORK label`  
**Description**: Create parallel execution path (not yet implemented)  
**Example**: `FORK worker`

### JOIN
**Syntax**: `JOIN`  
**Description**: Wait for forked paths to complete (not yet implemented)  
**Example**: `JOIN`

### HALT
**Syntax**: `HALT`  
**Description**: Stop program execution  
**Example**: `HALT`

## Memory/IO Operations (8)

### LOAD
**Syntax**: `LOAD address`  
**Description**: Load value from memory onto stack  
**Example**: `LOAD @1000`

### STORE
**Syntax**: `STORE address`  
**Description**: Store top of stack to memory  
**Stack**: `[value] → []` (value removed)  
**Example**: `PUSH #42` / `STORE @result`

### FOPEN
**Syntax**: `FOPEN filename [mode]`  
**Description**: Open file for operations (not yet implemented)  
**Example**: `FOPEN "data.txt" "r"`

### FREAD
**Syntax**: `FREAD`  
**Description**: Read from open file (not yet implemented)  
**Example**: `FREAD`

### FWRITE
**Syntax**: `FWRITE`  
**Description**: Write to open file (not yet implemented)  
**Example**: `FWRITE`

### FCLOSE
**Syntax**: `FCLOSE`  
**Description**: Close open file (not yet implemented)  
**Example**: `FCLOSE`

### LLMGEN
**Syntax**: `LLMGEN prompt`  
**Description**: Generate code using local LLM (not yet implemented)  
**Example**: `LLMGEN "create a sorting function"`

### EVOLVE
**Syntax**: `EVOLVE error_context`  
**Description**: Trigger self-improvement based on error (not yet implemented)  
**Example**: `EVOLVE "stack underflow in sort"`

## Usage Examples

### Calculate Fibonacci Number
```assembly
; Calculate 8th Fibonacci number
PUSH #0     ; F(0)
PUSH #1     ; F(1)
PUSH #6     ; Counter (n-2)

fib_loop:
    OVER    ; Copy F(n-2)
    OVER    ; Copy F(n-1)
    ADD     ; F(n) = F(n-1) + F(n-2)
    SWAP    ; Reorder stack
    DROP    ; Remove old F(n-2)
    PUSH #1
    SUB     ; Decrement counter
    DUP
    JNZ fib_loop
    
DROP        ; Remove counter
HALT        ; Result on stack
```

### Recursive Factorial
```assembly
factorial:
    DUP         ; Duplicate n
    PUSH #1
    SUB         ; n-1
    DUP         ; Check if zero
    JZ base_case
    CALL factorial
    MUL         ; n * factorial(n-1)
    RET
    
base_case:
    DROP        ; Remove 0
    PUSH #1     ; 0! = 1
    RET

main:
    PUSH #5     ; Calculate 5!
    CALL factorial
    HALT
```