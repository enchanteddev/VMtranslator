import sys

from Parser import Parser, CommandType as CT
from CodeWriter import CodeWriter

class VMTranslator:
    def __init__(self, fp) -> None:
        self.parser = Parser(fp)
        self.cw = CodeWriter(fp)

    def translate(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            cmdT = self.parser.commandType()
            if cmdT == CT.C_ARITHMETIC:
                self.cw.writeArithmetic(self.parser.curr)
            elif cmdT == CT.C_PUSH or cmdT == CT.C_POP:
                self.cw.writePushPop(self.parser.commandType(), self.parser.arg1(), self.parser.arg2())
        self.cw.close()

VMTranslator(sys.argv[1]).translate()