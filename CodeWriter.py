from Parser import CommandType as CT


segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
            'pointer': 'pointer'}


with open('HackTemplates/Arithmetic/binary.asm') as f: binaryTemplate = f.read()
with open('HackTemplates/Arithmetic/unary.asm') as f: unaryTemplate = f.read()
with open('HackTemplates/Arithmetic/compare.asm') as f: compareTemplate = f.read()
with open('HackTemplates/Stack/pushD.asm') as f: pushD = f.read()
with open('HackTemplates/Stack/popD.asm') as f: popD = f.read()
with open('HackTemplates/Stack/push.asm') as f: pushTemplate = f.read()
with open('HackTemplates/Stack/pop.asm') as f: popTemplate = f.read()


class CodeWriter:
    def __init__(self, fp: str) -> None:
        self.fp = fp
        self.name = '.'.join(fp.split('.')[:-1])
        self._res = ""
        self.ind = 0

    def writeArithmetic(self, instruction: str):
        translated = ''

        match instruction:
            case 'add': translated += binaryTemplate.format(op = '+')
            case 'sub': translated += binaryTemplate.format(op = '-')
            case 'and': translated += binaryTemplate.format(op = '&')
            case 'or': translated += binaryTemplate.format(op = '|')
            case 'lt': translated += compareTemplate.format(jmp = f'@true{self.ind}\nD;JLT', ind = self.ind) + '\n' + pushD; self.ind += 1
            case 'gt': translated += compareTemplate.format(jmp = f'@true{self.ind}\nD;JGT', ind = self.ind) + '\n' + pushD; self.ind += 1
            case 'eq': translated += compareTemplate.format(jmp = f'@true{self.ind}\nD;JEQ', ind = self.ind) + '\n' + pushD; self.ind += 1
            # case 'neg': translated += compareTemplate.format(jmp = f'@true{self.ind}\nD;JNE', ind = self.ind) + '\n' + pushD; self.ind += 1
            case 'neg': translated += unaryTemplate.format(op = '-')
            case 'not': translated += unaryTemplate.format(op = '!')
        translated += '\n'
        self._res += translated
    
    def writePushPop(self, command, segment: str, index: int):
        seg = ''
        match segment:
            case 'constant': pass
            case 'static':
                seg += f'@{self.name}.{index}\nA=D+M\nD=M\n'
            case 'temp':
                index += 5
            case _:
                seg += f'@{segments[segment]}\nD=D+M\n'
        
        translated = pushTemplate.format(val = index, seg = seg)
        match command:
            case CT.C_PUSH: translated += pushD
            case CT.C_POP: translated += popD
        
        translated += '\n'
        self._res += translated
    
    def close(self):
        with open(self.name + '.asm', 'w') as wf:
            wf.write(self._res)