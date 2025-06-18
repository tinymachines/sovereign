# Your First PROJECT SOVEREIGN Program

Let's write and run your first PROJECT SOVEREIGN program!

## Objectives
- Write a simple program
- Understand basic operations
- Run the program
- Debug common issues

## Prerequisites
- PROJECT SOVEREIGN installed
- Basic command line knowledge

## Hello, Stack!

Let's start with the traditional first program - calculating 42 (the answer to everything).

### Step 1: Create the Program

Create a file named `answer.sov`:

```assembly
; answer.sov - Calculate the answer to everything
; Demonstrates basic arithmetic and stack operations

PUSH #40        ; Push 40 onto the stack
PUSH #2         ; Push 2 onto the stack
ADD             ; Add them together (40 + 2 = 42)
DUP             ; Duplicate the result
STORE @answer   ; Store one copy in memory
HALT            ; Stop execution
```

### Step 2: Run the Program

```bash
sovereign run answer.sov
```

Expected output:
```
Executing program...
Execution completed successfully
```

### Step 3: Debug Mode

Run with debug flag to see what happened:

```bash
sovereign run answer.sov --debug
```

This shows:
- Source code with line numbers
- Final VM state
- Stack contents: [42]
- Memory contents: @answer = 42

## Understanding the Program

Let's trace through each instruction:

| Step | Instruction | Stack Before | Stack After | Memory |
|------|------------|--------------|-------------|---------|
| 1 | `PUSH #40` | `[]` | `[40]` | `{}` |
| 2 | `PUSH #2` | `[40]` | `[40, 2]` | `{}` |
| 3 | `ADD` | `[40, 2]` | `[42]` | `{}` |
| 4 | `DUP` | `[42]` | `[42, 42]` | `{}` |
| 5 | `STORE @answer` | `[42, 42]` | `[42]` | `{answer: 42}` |
| 6 | `HALT` | `[42]` | `[42]` | `{answer: 42}` |

## A More Complex Example

Let's calculate the factorial of 5:

```assembly
; factorial.sov - Calculate 5!
; Demonstrates functions and recursion

main:
    PUSH #5           ; Calculate 5!
    CALL factorial    ; Call factorial function
    HALT             ; Result: 120 on stack

factorial:
    DUP              ; Duplicate n
    PUSH #1          ; 
    SUB              ; n-1
    DUP              ; Check if zero
    JZ base_case     ; If n-1 = 0, go to base case
    
    CALL factorial   ; Recursive call with n-1
    MUL              ; n * factorial(n-1)
    RET              ; Return to caller
    
base_case:
    DROP             ; Remove the 0
    PUSH #1          ; 0! = 1 and 1! = 1
    RET              ; Return to caller
```

Run it:
```bash
sovereign run factorial.sov --debug
```

## Interactive Development

Use the REPL to experiment:

```bash
sovereign repl
```

Try these commands:
```
sovereign> PUSH #10
sovereign> PUSH #20
sovereign> ADD
sovereign> state
```

The `state` command shows:
- Data Stack: [30]
- Control Stack: []
- Program Counter: 0

## Common Patterns

### Pattern 1: Save and Restore
```assembly
DUP              ; Save value
CALL process     ; Might modify stack
SWAP             ; Bring original back
DROP             ; Remove processed
```

### Pattern 2: Conditional Execution
```assembly
PUSH #10
PUSH #10
SUB              ; Compare values
JZ equal         ; Jump if equal

; Not equal
PUSH #0
JMP done

equal:
PUSH #1

done:
; Continue...
```

### Pattern 3: Loop Counter
```assembly
PUSH #5          ; Loop 5 times

loop:
    DUP          ; Preserve counter
    JZ done      ; Exit if zero
    
    ; Loop body
    PUSH #42
    DROP
    
    PUSH #1
    SUB          ; Decrement
    JMP loop
    
done:
    DROP         ; Clean up counter
```

## Debugging Tips

### 1. Check Your Stack
Most errors come from stack imbalance:
```assembly
; BAD - Forgets to push second operand
PUSH #42
ADD          ; ERROR: Not enough values

; GOOD
PUSH #42
PUSH #10
ADD
```

### 2. Validate Jumps
Ensure labels exist:
```assembly
JMP nowhere  ; ERROR: Undefined label

correct:
JMP done     ; OK: Label exists
; ...
done:
HALT
```

### 3. Memory Addresses
Use valid hex addresses:
```assembly
STORE @G00D   ; ERROR: G is not hex
STORE @F00D   ; OK: Valid hex
```

## Exercises

### Exercise 1: Calculate 2^8
Write a program to calculate 2 to the power of 8 using multiplication.

<details>
<summary>Solution</summary>

```assembly
; power.sov - Calculate 2^8
PUSH #2          ; Base
PUSH #7          ; We'll multiply 7 more times

power_loop:
    PUSH #2      ; Multiplier
    MUL          ; Result * 2
    SWAP         ; Bring counter to top
    PUSH #1
    SUB          ; Decrement counter
    DUP
    JNZ power_loop
    
DROP             ; Remove counter
HALT             ; Result: 256
```
</details>

### Exercise 2: Sum 1 to 10
Calculate the sum of numbers from 1 to 10.

<details>
<summary>Solution</summary>

```assembly
; sum.sov - Sum 1 to 10
PUSH #0          ; Sum accumulator
PUSH #10         ; Counter

sum_loop:
    DUP          ; Copy counter
    ROT          ; Bring sum to top
    ADD          ; Add counter to sum
    SWAP         ; Put counter back on top
    PUSH #1
    SUB          ; Decrement
    DUP
    JNZ sum_loop
    
DROP             ; Remove counter
HALT             ; Result: 55
```
</details>

### Exercise 3: Find Maximum
Given two values, find the maximum.

<details>
<summary>Solution</summary>

```assembly
; max.sov - Find maximum of two values
PUSH #42         ; First value
PUSH #37         ; Second value

; Compare by subtraction
OVER             ; Copy first value
OVER             ; Copy second value
SUB              ; first - second
JZ equal         ; If 0, they're equal
JNZ check_sign   ; If not 0, check which is bigger

equal:
    DROP         ; Remove one (they're equal)
    JMP done

check_sign:
    ; If result is negative, second is bigger
    DUP          ; Duplicate difference
    PUSH #0
    SWAP
    SUB          ; 0 - difference (negates)
    JZ first_bigger
    
    ; Second is bigger
    DROP         ; Remove difference
    SWAP         ; Put second on top
    DROP         ; Remove first
    JMP done
    
first_bigger:
    DROP         ; Remove difference
    DROP         ; Remove second
    
done:
    HALT         ; Maximum on stack
```
</details>

## Next Steps

Now that you've written your first programs:
1. Read [Understanding Stacks](stacks.md) to master stack manipulation
2. Explore [Control Flow](control-flow.md) for advanced branching
3. Try [Working with Memory](memory.md) for data persistence

Congratulations on your first PROJECT SOVEREIGN program!