# Execution Model

PROJECT SOVEREIGN uses a stack-based execution model with dual stacks and addressable memory.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  PROGRAM MEMORY                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Instructions (Code Segment)               │  │
│  │ - PUSH #42                                │  │
│  │ - ADD                                     │  │
│  │ - HALT                                    │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Data Memory (Heap)                        │  │
│  │ @0000: ...                                │  │
│  │ @1000: 42                                 │  │
│  │ @FFFF: ...                                │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐
│   DATA STACK    │    │  CONTROL STACK  │
├─────────────────┤    ├─────────────────┤
│       42        │←TOP│   return_addr   │←TOP
│       10        │    │   saved_pc      │
│       ...       │    │      ...        │
└─────────────────┘    └─────────────────┘

┌─────────────────────────────────────────────────┐
│                   REGISTERS                      │
│  PC: 0x0003   SP: 0x0002   r0: 0   r1: 42      │
└─────────────────────────────────────────────────┘
```

## Stack Operations

### Data Stack
- **Purpose**: Holds operands and results
- **Operations**: PUSH, POP, DUP, SWAP, etc.
- **Growth**: Grows upward (push increases size)
- **Underflow**: Error when popping from empty stack

### Control Stack
- **Purpose**: Holds return addresses for CALL/RET
- **Operations**: Automatically managed by CALL/RET
- **Isolation**: Separate from data stack for security

## Execution Cycle

1. **Fetch**: Read instruction at Program Counter (PC)
2. **Decode**: Parse opcode and operands
3. **Execute**: Perform operation
4. **Update**: Increment PC (unless jump/call)

```python
while running:
    instruction = program[PC]
    opcode = decode(instruction)
    execute(opcode)
    if not jumped:
        PC += 1
```

## Memory Model

### Address Space
- **Size**: 16-bit addresses (0x0000 - 0xFFFF)
- **Format**: Hexadecimal (@1000, @BEEF)
- **Access**: LOAD and STORE operations

### Memory Regions
```
0x0000 - 0x00FF : System reserved
0x0100 - 0x0FFF : Stack space
0x1000 - 0xEFFF : User data
0xF000 - 0xFFFF : Memory-mapped I/O
```

## Control Flow

### Sequential Execution
Instructions execute in order unless redirected:
```assembly
PUSH #1    ; PC = 0
PUSH #2    ; PC = 1
ADD        ; PC = 2
HALT       ; PC = 3
```

### Jumps
Unconditional and conditional jumps modify PC:
```assembly
    JMP target      ; PC = address of 'target'
    JZ zero_handler ; Jump only if top of stack is 0
    JNZ loop        ; Jump only if top of stack is not 0
```

### Function Calls
CALL pushes return address, RET pops it:
```assembly
main:
    PUSH #42
    CALL function   ; Push PC+1 to control stack
    HALT           ; PC+1: Continue here after RET

function:
    DUP
    RET            ; Pop return address to PC
```

## Register Model

### Special Registers
- **PC**: Program Counter - current instruction
- **SP**: Stack Pointer - top of data stack
- **CS**: Control Stack pointer

### General Registers
- **r0 - r15**: General purpose registers
- **Access**: Direct read/write
- **Usage**: Temporary storage, parameters

## Error Handling

### Runtime Errors
1. **Stack Underflow**: Pop from empty stack
2. **Stack Overflow**: Exceed stack capacity
3. **Invalid Address**: Access outside memory
4. **Division by Zero**: DIV with zero divisor
5. **Invalid Opcode**: Unknown instruction

### Error Response
```assembly
; Error handler pattern
error_handler:
    PUSH #-1        ; Error code
    STORE @error    ; Save error state
    HALT           ; Stop execution
```

## Concurrency Model (Future)

### FORK/JOIN Semantics
```assembly
main:
    PUSH #data1
    FORK worker1    ; Create parallel path
    PUSH #data2
    FORK worker2    ; Create another path
    
    ; Main continues
    CALL process_main
    
    JOIN           ; Wait for all forks
    HALT

worker1:
    ; Parallel execution
    CALL process1
    RET            ; Mark fork complete

worker2:
    ; Parallel execution
    CALL process2
    RET            ; Mark fork complete
```

## Performance Characteristics

### Operation Costs
- **Stack ops**: O(1) - constant time
- **Arithmetic**: O(1) - constant time
- **Memory access**: O(1) - direct addressing
- **Jumps**: O(1) - direct PC update
- **Calls**: O(1) - stack push/pop

### Optimization Opportunities
1. **Peephole optimization**: Combine operations
2. **Dead code elimination**: Remove unreachable code
3. **Constant folding**: Evaluate at compile time
4. **Stack scheduling**: Minimize stack operations

## Example: Factorial Execution Trace

```assembly
factorial:          ; PC=0
    DUP            ; PC=1  Stack: [5,5]
    PUSH #1        ; PC=2  Stack: [5,5,1]
    SUB            ; PC=3  Stack: [5,4]
    DUP            ; PC=4  Stack: [5,4,4]
    JZ base        ; PC=5  Stack: [5,4,4] (not zero)
    CALL factorial ; PC=6  Control: [7], Jump to PC=0
    ; ... recursion ...
    MUL            ; PC=7  Stack: [5,24] → [120]
    RET            ; PC=8  Return to caller

base:              ; PC=9
    DROP           ; PC=10
    PUSH #1        ; PC=11
    RET            ; PC=12
```

## State Persistence

### Checkpointing
Programs can save state for recovery:
```assembly
checkpoint:
    ; Save stack to memory
    DUP
    STORE @stack_top
    ; Save registers
    PUSH r0
    STORE @saved_r0
    RET
```

### State Restoration
```assembly
restore:
    ; Restore registers
    LOAD @saved_r0
    POP r0
    ; Restore stack
    LOAD @stack_top
    RET
```