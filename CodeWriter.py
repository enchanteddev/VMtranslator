from Parser import CommandType as CT

with open('Hack/Arithmetic/binary.asm') as f: binaryT = f.read()
with open('Hack/Arithmetic/compare.asm') as f: compareT = f.read()
with open('Hack/Arithmetic/unary.asm') as f: unaryT = f.read()

with open('Hack/Stack/pushD.asm') as f: pushD = f.read()
with open('Hack/Stack/popD.asm') as f: popD = f.read()
with open('Hack/Stack/push.asm') as f: push = f.read()
with open('Hack/Stack/pop.asm') as f: pop = f.read()


segments = {'pointer': 'pointer', 'local': 'LCL', 'this': 'THIS', 'that': 'THAT', 'argument': 'ARG'}


class CodeWriter:
    def __init__(self, fp) -> None:
        self.fname = '.'.join(fp.split('/')[-1].split('.')[:-1])
        print(self.fname)
        self.fp = fp
        self._out = ''
        self._ind = 0

    def writeArithmetic(self, instr: str):
        translated = f'//{instr}\n'
        match instr:
            case 'add': translated += binaryT.format(op = '+')
            case 'sub': translated += binaryT.format(op = '-')
            case 'and': translated += binaryT.format(op = '&')
            case 'or': translated += binaryT.format(op = '|')

            case 'not': translated += unaryT.format(op = '!')
            case 'neg': translated += unaryT.format(op = '-')

            case 'eq':
                translated += compareT.format(jmp = f'@true{self._ind}\nD;JEQ', ind=self._ind) + '\n' + pushD
                self._ind += 1
            case 'lt':
                translated += compareT.format(jmp = f'@true{self._ind}\nD;JLT', ind=self._ind) + '\n' + pushD
                self._ind += 1
            case 'gt':
                translated += compareT.format(jmp = f'@true{self._ind}\nD;JGT', ind=self._ind) + '\n' + pushD
                self._ind += 1

        self._out += translated + '\n//-----------------\n'
    
    def writePushPop(self, command, segment, index):
        seg = ''
        if command == CT.C_PUSH:
            translated = f'//push {segment} {index}\n'

            match segment:
                case 'constant': pass
                case 'temp':
                    index += 5
                    seg += 'D=M\n'
                case 'static':
                    seg += f'@{self.fname}.{index}\nD=M\n'
                case 'pointer':
                    if index == 0: seg += f'@THIS\nD=M\n'
                    elif index == 1: seg += f'@THAT\nD=M\n'
                case _:
                    seg += f'@{segments[segment]}\nA=D+M\nD=M\n'
            translated += push.format(val = index, seg = seg)
            self._out += translated + pushD + '\n//-------------\n'

        if command == CT.C_POP:
            translated = f'//pop {segment} {index}\n'
            match segment:
                case 'temp':
                    index += 5
                case 'static':
                    seg += f'@{self.fname}.{index}\nD=A'
                case 'pointer':
                    if index == 0: seg += f'@THIS\nD=A'
                    elif index == 1: seg += f'@THAT\nD=A'
                case _:
                    seg += f'@{segments[segment]}\nD=D+M'
            translated += pop.format(ind = index, seg = seg) + '\n//--------------\n'
            self._out += translated

    def close(self):
        with open('.'.join(self.fp.split('.')[:-1]) + '.asm', 'w') as wf:
            wf.write(self._out)