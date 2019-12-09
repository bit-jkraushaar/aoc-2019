debug = 0

class Computer:

    def __init__(self, code, program_input):
        self.code = [ 0 if x >= len(code) else code[x] for x in range(100000) ]
        self.ptr = 0 # ptr: instruction pointer 
        self.program_output = []
        self.program_input = program_input
        self.state = "INITIALIZED"
        self.relative_base = 0
    
    def run(self):
        while(True):
            self.state = "RUNNING"
            [opcode, modes] = evaluate_instruction(self.code[self.ptr])
            if (opcode == 99):
                self.state = "TERMINATED"
                return
            elif (opcode == 1):
                modes.extend([0 for _ in range(3-len(modes))])
                summand_1 = self.get_parameter_by_mode(self.ptr+1, modes[0])
                summand_2 = self.get_parameter_by_mode(self.ptr+2, modes[1])
                if modes[2] == 0:
                    self.code[self.code[self.ptr+3]] = summand_1 + summand_2
                elif modes[2] == 2:
                    self.code[self.relative_base + self.code[self.ptr+3]] = summand_1 + summand_2
                self.ptr += 4
            elif (opcode == 2):
                modes.extend([0 for _ in range(3-len(modes))])
                factor_1 = self.get_parameter_by_mode(self.ptr+1, modes[0])
                factor_2 = self.get_parameter_by_mode(self.ptr+2, modes[1])
                if modes[2] == 0:
                    self.code[self.code[self.ptr+3]] = factor_1 * factor_2
                elif modes[2] == 2:
                    self.code[self.relative_base + self.code[self.ptr+3]] = factor_1 * factor_2
                self.ptr += 4
            elif (opcode == 3):
                modes.extend([0 for _ in range(1-len(modes))])
                if (len(self.program_input) == 0):
                    self.state = "WAITING_FOR_INPUT"
                    return # wait for input
                if (modes[0] == 0):
                    self.code[self.code[self.ptr+1]] = self.program_input.pop(0)
                elif (modes[0] == 2):
                    self.code[self.relative_base + self.code[self.ptr+1]] = self.program_input.pop(0)
                self.ptr += 2
            elif (opcode == 4):
                modes.extend([0 for _ in range(1-len(modes))])
                assert(len(modes) >= 1)
                output = self.get_parameter_by_mode(self.ptr+1, modes[0])
                if (debug):
                    print("Output:",str(output))
                self.program_output.append(output)
                self.ptr += 2
            elif (opcode == 5):
                modes.extend([0 for _ in range(2-len(modes))])
                value = self.get_parameter_by_mode(self.ptr+1, modes[0])
                jump_to = self.get_parameter_by_mode(self.ptr+2, modes[1])
                if value != 0:
                    self.ptr = jump_to
                else:
                    self.ptr += 3
            elif (opcode == 6):
                modes.extend([0 for _ in range(2-len(modes))])
                value = self.get_parameter_by_mode(self.ptr+1, modes[0])
                jump_to = self.get_parameter_by_mode(self.ptr+2, modes[1])
                if value == 0:
                    self.ptr = jump_to
                else:
                    self.ptr += 3
            elif (opcode == 7):
                modes.extend([0 for _ in range(3-len(modes))])
                operand_1 = self.get_parameter_by_mode(self.ptr+1, modes[0])
                operand_2 = self.get_parameter_by_mode(self.ptr+2, modes[1])
                if operand_1 < operand_2:
                    if (modes[2] == 0):
                        self.code[self.code[self.ptr+3]] = 1
                    elif (modes[2] == 2):
                        self.code[self.relative_base + self.code[self.ptr+3]] = 1
                else:
                    if (modes[2] == 0):
                        self.code[self.code[self.ptr+3]] = 0
                    elif (modes[2] == 2):
                        self.code[self.relative_base + self.code[self.ptr+3]] = 0
                self.ptr += 4
            elif (opcode == 8):
                modes.extend([0 for _ in range(3-len(modes))])
                operand_1 = self.get_parameter_by_mode(self.ptr+1, modes[0])
                operand_2 = self.get_parameter_by_mode(self.ptr+2, modes[1])
                if operand_1 == operand_2:
                    if (modes[2] == 0):
                        self.code[self.code[self.ptr+3]] = 1
                    elif (modes[2] == 2):
                        self.code[self.relative_base + self.code[self.ptr+3]] = 1
                else:
                    if (modes[2] == 0):
                        self.code[self.code[self.ptr+3]] = 0
                    elif (modes[2] == 2):
                        self.code[self.relative_base + self.code[self.ptr+3]] = 0
                self.ptr += 4
            elif (opcode == 9):
                modes.extend([0 for _ in range(1-len(modes))])
                offset_change = self.get_parameter_by_mode(self.ptr+1, modes[0])
                self.relative_base += offset_change
                self.ptr += 2
            else:
                print(self.program_output)
                raise Exception("Unknown opcode: " + str(opcode))
    
    def get_parameter_by_mode(self, ptr, mode):
        if mode == 0:
            return self.code[self.code[ptr]]
        elif mode == 1:
            return self.code[ptr]
        elif mode == 2:
            return self.code[self.relative_base + self.code[ptr]]
        else:
            raise Exception("Unknown mode: " + str(mode))

    def get_last_output(self):
        return self.program_output[len(self.program_output)-1]

    def get_whole_output(self):
        return self.program_output

    def provide_input(self, i):
        self.program_input.append(i)
    
    def has_terminated(self):
        return True if self.state == "TERMINATED" else False

    def get_state(self):
        return self.state

def evaluate_instruction(instruction):
    opcode_low = instruction % 10
    instruction = int(instruction / 10)
    opcode_high = instruction % 10
    opcode = opcode_high * 10 + opcode_low
    instruction = int(instruction / 10)
    
    modes = []
    while(instruction > 0):
        modes.append(instruction % 10)
        instruction = int(instruction / 10)
        
    return [opcode, modes]