from Parser import Parser, CommandType as CT
from CodeWriter import CodeWriter

class VMTranslater:
    def __init__(self, fp: str) -> None:
        self.parser = Parser(fp)
        self.cw = CodeWriter(fp)
    
    def translate(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            instrType = self.parser.commandType()
            if instrType == CT.C_POP or instrType == CT.C_PUSH:
                self.cw.writePushPop(instrType, self.parser.arg1(), int(self.parser.arg2()))
            if instrType == CT.C_ARITHMETIC:
                self.cw.writeArithmetic(self.parser.current)
        self.cw.close()

# VMTranslater('/home/krawat/random software from internet/n2t/nand2tetris/projects/07/StackArithmetic/StackTest/StackTest.vm').translate()
VMTranslater('/home/krawat/random software from internet/n2t/nand2tetris/projects/07/StackArithmetic/StackTest/StackTest.vm').translate()