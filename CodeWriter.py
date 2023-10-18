from pathlib import Path

from Parser import CommandType as CT


with open('Hack/Arithmetic/binary.asm') as f: binaryT = f.read()
with open('Hack/Arithmetic/compare.asm') as f: compareT = f.read()
with open('Hack/Arithmetic/unary.asm') as f: unaryT = f.read()

with open('Hack/Stack/pushD.asm') as f: pushD = f.read()
with open('Hack/Stack/popD.asm') as f: popD = f.read()
with open('Hack/Stack/push.asm') as f: push = f.read()
with open('Hack/Stack/pop.asm') as f: pop = f.read()

with open('Hack/Function/call.asm') as f: callBody = f.read()
with open('Hack/Function/return.asm') as f: returnBody = f.read()
with open('Hack/Function/frameD.asm') as f: frameD = f.read()


segments = {'pointer': 'pointer', 'local': 'LCL', 'this': 'THIS', 'that': 'THAT', 'argument': 'ARG'}


class CodeWriter:
    def __init__(self, fp, save = None) -> None:
        fp = str(fp)
        self.fname = '.'.join(fp.split('/')[-1].split('.')[:-1])
        print(self.fname, save)
        self.fp = fp
        self.save = save
        # self._out = ''
        self._out = '@256\nD=A\n@SP\nM=D\n'
        self._truefalse_ind = 0
        self._call_ctr = 0
        self.writeCall('Sys.init', 0)

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
                translated += compareT.format(jmp = f'@true{self._truefalse_ind}\nD;JEQ', ind=self._truefalse_ind) + '\n' + pushD
                self._truefalse_ind += 1
            case 'lt':
                translated += compareT.format(jmp = f'@true{self._truefalse_ind}\nD;JLT', ind=self._truefalse_ind) + '\n' + pushD
                self._truefalse_ind += 1
            case 'gt':
                translated += compareT.format(jmp = f'@true{self._truefalse_ind}\nD;JGT', ind=self._truefalse_ind) + '\n' + pushD
                self._truefalse_ind += 1

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

    def writeLabel(self, label: str):
        self._out += f'({label})\n'
    
    def writeGoto(self, label: str):
        self._out += f'@{label}\n0;JMP\n'

    def writeIf(self, label: str):
        self._out += popD + f'\n@{label}\nD;JNE\n'

    def writeFunction(self, fnName: str, nVars: int):
        self.writeLabel(fnName)
        self._out += 'D=0\n' + (pushD + '\n') * nVars

    def writeCall(self, fnName: str, nArgs: int):
        self._out += f'@ret{self._call_ctr}\nD=A\n' + pushD + '\n'
        pointers = ['LCL', 'ARG', 'THIS', 'THAT']
        for ptr in pointers:
            self._out += f'@{ptr}\nD=M\n' + pushD + '\n'
        self._out += callBody.format(arg5 = 5 + nArgs, fn = fnName)
        self._out += f'\n(ret{self._call_ctr})\n'
        self._call_ctr += 1

    def writeReturn(self):
        ret = frameD.format(ind = 5) + '\n@ret\nM=D'
        pointers = ['LCL', 'ARG', 'THIS', 'THAT']
        restore = ''
        for ind, ptr in enumerate(pointers):
            restore += frameD.format(ind = 4 - ind) + f'\n@{ptr}\nM=D\n'
        self._out += returnBody.format(retaddr = ret, restore = restore, pop=popD) + '\n'

    def close(self):
        if self.save:
            with open(self.save, 'a') as wf:
                wf.write(self._out)
            return
        print('.'.join(self.fp.split('.')[:-1]) + '.asm')
        with open('.'.join(self.fp.split('.')[:-1]) + '.asm', 'a') as wf:
            wf.write(self._out)