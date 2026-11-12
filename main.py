from lexer import tokenize
from syntax import runParser

def main():
    with open("input.txt","r") as f:
        sourceCode= f.read()
    tkns= tokenize(sourceCode)
    with open("output.txt","w") as f:
        for tknType , lexeme , lineNo in tkns:
            f.write(f"Token  :  {tknType}\n")
            f.write(f"Lexeme :  {lexeme}\n")
            f.write(f"Line No:  {lineNo}\n\n")
        print("Lexer has run successfully! --> Open output.txt")
    runParser("output.txt")

main()