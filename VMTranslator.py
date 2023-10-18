import sys
from pathlib import Path

from Parser import Parser, CommandType as CT
from CodeWriter import CodeWriter

class VMTranslator:
    def __init__(self, inF, outF):
        self.parser = Parser(inF)
        self.cw = CodeWriter(inF, outF)

    def translate(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            cmdT = self.parser.commandType()
            if cmdT == CT.C_ARITHMETIC:
                self.cw.writeArithmetic(self.parser.curr)
            elif cmdT == CT.C_PUSH or cmdT == CT.C_POP:
                self.cw.writePushPop(self.parser.commandType(), self.parser.arg1(), self.parser.arg2())
            elif cmdT == CT.C_FUNCTION:
                self.cw.writeFunction(self.parser.arg1(), self.parser.arg2())
            elif cmdT == CT.C_CALL:
                self.cw.writeCall(self.parser.arg1(), self.parser.arg2())
            elif cmdT == CT.C_RETURN:
                self.cw.writeReturn()
            elif cmdT == CT.C_GOTO:
                self.cw.writeGoto(self.parser.arg1())
            elif cmdT == CT.C_IF:
                self.cw.writeIf(self.parser.arg1())
            elif cmdT == CT.C_LABEL:
                self.cw.writeLabel(self.parser.arg1())
        self.cw.close()

path = Path(sys.argv[1])
if path.is_file() and path.suffix == '.vm':
    vmt = VMTranslator(path, path)
    try:
        vmt.translate()
    except Exception as e:
        print(e, vmt.parser.curr)
        quit()
else:
    for p in path.iterdir():
        if p.is_file() and p.suffix == '.vm':
            vmt = VMTranslator(p, path / (path.name + '.vm'))
            try:
                vmt.translate()
            except Exception as e:
                print(e, vmt.parser.curr)
                quit()