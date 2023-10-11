from enum import Enum, auto


class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()


class Parser:
    def __init__(self, fp: str) -> None:
        with open(fp) as f:
            self.lines = f.readlines()
        self.cursor = -1
        self.end = len(self.lines)

        self.current = ''
        self.segments = self.current.split(' ')
    
    def hasMoreLines(self):
        return self.cursor < self.end - 1
    
    def advance(self):
        self.cursor += 1
        self.current = self.lines[self.cursor]
        while self.cursor < self.end - 1 and (self.current.startswith('//') or self.current.strip() == ''):
            self.cursor += 1
            self.current = self.lines[self.cursor]
        self.current = self.current.split('//')[0].strip()
        self.segments = self.current.split(' ')
    
    def commandType(self) -> CommandType:
        first_part = self.segments[0]
        match first_part:
            case 'push': return CommandType.C_PUSH
            case 'pop': return CommandType.C_POP
            case 'label': return CommandType.C_LABEL
            case 'goto': return CommandType.C_GOTO
            case 'if-goto': return CommandType.C_IF
            case 'Function': return CommandType.C_FUNCTION
            case 'Call': return CommandType.C_CALL
            case 'return': return CommandType.C_RETURN
            case 'add': return CommandType.C_ARITHMETIC
            case 'and': return CommandType.C_ARITHMETIC
            case 'or': return CommandType.C_ARITHMETIC
            case 'not': return CommandType.C_ARITHMETIC
            case 'sub': return CommandType.C_ARITHMETIC
            case 'neg': return CommandType.C_ARITHMETIC
            case 'eq': return CommandType.C_ARITHMETIC
            case 'gt': return CommandType.C_ARITHMETIC
            case 'lt': return CommandType.C_ARITHMETIC
            case _: raise ValueError(f"line {self.cursor}: {self.current}; invalid first token {first_part}")
        
    def arg1(self):
        if len(self.segments) < 2:
            return self.segments[0]
        return self.segments[1]
    
    def arg2(self):
        try:
            return self.segments[2]
        except IndexError:
            raise Exception(f"line {self.cursor}: {self.current}; called arg2")