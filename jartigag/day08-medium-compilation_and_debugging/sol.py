#!/usr/bin/env python

input = [line.strip() for line in open("input").readlines()]

def run_boot_code(print_lines=False):
    already_read = []
    pos = 0
    accumulator = 0

    while pos not in already_read:
        try:
            i,n = input[pos].split()
            already_read.append(pos)
            if i=="acc":
                accumulator+=int(n)
            if print_lines:
                print(pos,"\t",input[pos],"\t",accumulator)
            if i=="jmp":
                pos+=int(n)
            else:
                pos+=1
        except IndexError:
            return already_read, accumulator

    return already_read, accumulator

executed_instructions_linenumbers, accumulator1 = run_boot_code()

print(f"accumulator1: {accumulator1}")

original_input = input.copy()

for l in executed_instructions_linenumbers:
    input = original_input.copy()
    i,n = input[l].split()
    if i=="jmp":
            input[l] = f"nop {n}"
            exec_instr_linenum, accumulator2 = run_boot_code()
            if  exec_instr_linenum[-1] == (len(input)-1):
                print(f'"{original_input[l]} -> {input[l]}" (line {l}, indexing in 0)')
                print(f'accumulator2: {accumulator2}')
                break
