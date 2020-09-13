"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = [0] * 8

        self.running = True

    def load(self, filename):
        print(filename)
        # Open a file and load into memory
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    # Split the current line on the # symbol
                    split_line = line.split('#')
                    code_value = split_line[0].strip() # removes whitespace and \n character
                    # Make sure that the value before the # symbol is not empty
                    if code_value == '':
                        continue
                    num = int(code_value, 2)
                    self.ram[address] = num
                    address += 1
        except FileNotFoundError: 
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        HLT = 0b00000001
        PRN = 0b01000111
        MUL = 0b10100010
        CMP = 0b10100111

        self.running = True

        self.load(sys.argv[1])

        while self.running:
            instruction = self.ram_read(self.pc)
            # print(instruction)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.running = False
                self.pc += 1
                print("in HLT")

            elif instruction == LDI:
                print("in LDI")
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN:
                val = self.ram_read(self.pc + 1)
                print(self.reg[val])
                print("in PRN")
                self.pc += 2

            elif instruction == MUL:
                print("in MUL")
                result = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = result
                self.pc += 3

            elif instruction == CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.fl &= 0b00000100
                elif self.reg[operand_a] < self.reg[operand_b]:
                    self.fl &= 0b00000010
                elif self.reg[operand_a] > self.reg[operand_b]:
                    self.fl &= 0b00000001

            elif instruction == JMP:
                pass

            elif instruction == JEQ:
                pass

            elif instruction == JNE:
                pass

            else:
                print(f"Unknown instruction {instruction}")
                sys.exit(1)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr        