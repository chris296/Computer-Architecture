"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.register = [0] * 8
        self.running = True
        self.fl = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment = line.split("#")
                    command = comment[0].strip()

                    if command == "":
                        continue

                    num = int(command, 2)

                    self.ram[address] = num
                    address += 1

        except:
            print(f"{sys.argv[0]} / {sys.argv[1]} not found")


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        SP = 7
        ADD = 0b10100000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while self.running:
            IR = self.ram_read(self.pc)

            operandA = self.ram_read(self.pc + 1)
            operandB = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.running = False

            elif IR == LDI:
                address = operandA
                value = operandB
                self.register[address] = value
                self.pc += 3
                
            elif IR == PRN:
                address = operandA
                value = self.register[address]
                print(value)
                self.pc += 2

            elif IR == MUL:
                self.alu("MUL", operandA, operandB)
                self.pc += 3

            elif IR == ADD:
                self.alu("ADD", operandA, operandB)
                self.pc += 3

            elif IR == PUSH:
                self.register[SP] -= 1
                sp = self.register[SP]
                value = self.register[operand_a]
                self.ram[sp] = value
                self.pc += 2
            
            elif IR == POP:
                sp = self.register[SP]
                value = self.ram[sp]
                self.register[operand_a] = value
                self.register[SP] += 1
                self.pc += 2

            elif IR == CALL:
                self.register[SP] -= 1
                sp = self.register[SP]
                self.ram[sp] = self.pc + 2
                self.pc = self.register[operandA]

            elif IR == RET:
                sp = self.register[SP]
                self.pc = self.ram[sp]
                self.register[SP] += 1

            elif IR == CMP:
                valuea = self.register[operandA]
                valueb = self.register[operandB]
                if valuea == valueb:
                    self.fl = 1
                elif valuea > valueb:
                    self.fl =  2
                elif valuea < valueb:
                    self.fl = 4
                self.pc += 3

            elif IR == JNE:
                if self.fl == 1:
                    self.pc += 2
                elif self.fl != 1:
                    self.pc = self.register[operandA]
            
            elif IR == JMP:
                self.pc = self.register[operandA]
            
            elif IR == JEQ:
                if self.fl != 1:
                    self.pc += 2
                elif self.fl == 1:
                    self.pc = self.register[operandA]

            else:
                self.running = False
                sys.exit()



