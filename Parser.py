from enum import Enum, auto

class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_GOTO = auto()
    C_RETURN = auto()
    C_CALL = auto()



class Parser:
    def __init__(self, path) -> None:
        with open(path) as f:
            self.lines = f.readlines()
        ll = []
        for l in self.lines:
            if (ls := l.strip()) != '':
                ll.append(ls)
        self.lines = ll
        self.cursor = -1
        self.curr = ''
        self._tokens = []
        self.end = len(self.lines)
    
    def hasMoreLines(self):
        return self.cursor < self.end - 1
    
    def advance(self):
        self.cursor += 1
        while (curr := self.lines[self.cursor])[:2] == '//':
            self.cursor += 1
            if not self.hasMoreLines(): break
        self.curr = curr.split('//')[0].strip()
        self._tokens = self.curr.split(' ')
        print(self._tokens)
    
    def commandType(self):
        match self._tokens[0]:
            case 'add': return CommandType.C_ARITHMETIC
            case 'sub': return CommandType.C_ARITHMETIC
            case 'neg': return CommandType.C_ARITHMETIC
            case 'eq': return CommandType.C_ARITHMETIC
            case 'gt': return CommandType.C_ARITHMETIC
            case 'lt': return CommandType.C_ARITHMETIC
            case 'or': return CommandType.C_ARITHMETIC
            case 'not': return CommandType.C_ARITHMETIC
            case 'and': return CommandType.C_ARITHMETIC

            case 'label': return CommandType.C_LABEL
            case 'if-goto': return CommandType.C_IF
            case 'goto': return CommandType.C_GOTO

            case 'function': return CommandType.C_FUNCTION
            case 'return': return CommandType.C_RETURN
            case 'call': return CommandType.C_CALL

            case 'push': return CommandType.C_PUSH
            case 'pop': return CommandType.C_POP
            case _: raise SyntaxError(f"{self.cursor}: {self.curr}; invalid first token")
        
    def arg1(self):
        if self.commandType() == CommandType.C_ARITHMETIC:
            return self._tokens[0]
        return self._tokens[1]
    
    def arg2(self):
        return int(self._tokens[2])