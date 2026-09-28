from lexer import tokenize

def main():
    with open("input.txt","r") as f:
        sourceCode= f.read()
    tkns= tokenize(sourceCode)
    with open("output.txt","w") as f:
            # f.write(f"{'Token':<15}{'Lexeme':<15}{'Line No'}\n")
        for tknType , lexeme , lineNo in tkns:
            f.write(f"Token  :  {tknType}\n")
            f.write(f"Lexeme :  {lexeme}\n")
            f.write(f"Line No:  {lineNo}\n\n")
main()
