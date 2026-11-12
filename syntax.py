def loadTokens(fileName):
    tokens = []
    tType = ""
    lex = ""
    with open(fileName, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip("\n")
        if line.startswith("Token"):
            tType = line.split(":", 1)[1].strip()
        elif line.startswith("Lexeme"):
            lex = line.split(":", 1)[1].strip()
        elif line.startswith("Line No"):
            ln = int(line.split(":", 1)[1].strip())
            if tType == "Error":
                errors.append(("Lexical error: " + lex, ln))
            else:
                tokens.append((tType, lex, ln))
    return tokens


tokens = []
pos = 0
symTable = []
errors = []
OPS = ["+", "-", "/", "*", ">", "<", "=", "=="]
TYPES = ["void", "char", "int"]

def current():
    if pos < len(tokens):
        return tokens[pos]
    if len(tokens) > 0:
        return ("EOF", "", tokens[-1][2])
    return ("EOF", "", 0)

def advance():
    global pos
    pos += 1

def lexemeIs(text):
    t = current()
    if t[0] == "Keyword":
        return t[1].lower() == text
    return t[1] == text

def isType():
    t = current()
    return t[0] == "Keyword" and t[1].lower() in TYPES

def isOperator():
    t = current()
    return t[0] == "Operator" and t[1] in OPS

def isConstant():
    return current()[0] in ("Number", "Char")

def isIdentifier():
    return current()[0] == "Identifier"

def syntaxError(msg, missing=True):
    errLine = current()[2]
    # missing    eeror 
    if missing and pos > 0 and pos <= len(tokens) and tokens[pos-1][2] < errLine:
        errLine = tokens[pos-1][2]
    errors.append((msg, errLine))
    while pos < len(tokens) and tokens[pos][2] == errLine:
        advance()

def expect(text, msg):
    if lexemeIs(text):
        advance()
        return True
    syntaxError(msg)
    return False


def initDeclList(typeName, scope):
    while True:
        if not isIdentifier():
            syntaxError("Identifier expected")
            return
        name = current()[1]
        advance()

        arraySize = ""
        if lexemeIs("["):
            advance()
            arraySize = 0
            if current()[0] == "Number":
                arraySize = int(current()[1])
                advance()
            if not expect("]", "Right bracket ']' expected"):
                return

        symTable.append((name, typeName.capitalize(), scope, arraySize))

        if lexemeIs("="):
            advance()
            if isConstant():
                advance()
            else:
                syntaxError("Constant expected after '='")
                return

        if lexemeIs(","):
            advance()
        elif lexemeIs(";"):
            advance()
            return
        else:
            syntaxError("Semicolon expected")
            return

def expression():
    if not isIdentifier():
        syntaxError("Identifier expected")
        return False
    advance()
    if not isOperator():
        syntaxError("Operator expected")
        return False
    advance()
    if isIdentifier():
        advance()
        if isOperator():
            advance()
            if isIdentifier() or isConstant():
                advance()
            else:
                syntaxError("Identifier or constant expected")
                return False
    elif isConstant():
        advance()
    else:
        syntaxError("Identifier or constant expected")
        return False
    return True

def block(scope):
    if not expect("{", "Opening brace '{' expected"):
        return False
    while current()[0] != "EOF" and not lexemeIs("}"):
        statement(scope)
    return expect("}", "Closing brace '}' expected")

def statement(scope):
    if isType():
        typeName = current()[1]
        advance()
        initDeclList(typeName, scope)
    elif lexemeIs("if"):
        selectionStatement(scope)
    elif lexemeIs("while"):
        whileStatement(scope)
    elif lexemeIs("for"):
        forStatement(scope)
    elif lexemeIs("do"):
        doStatement(scope)
    elif lexemeIs(";"):
        advance()
    elif lexemeIs("{"):
        block(scope)
    elif isIdentifier():
        if expression():
            expect(";", "Semicolon expected")
    else:
        syntaxError("Unexpected token '" + current()[1] + "'", False)


def selectionStatement(scope):
    advance()
    if not expect("(", "Opening parenthesis '(' expected"):
        return
    if not expression():
        return
    if not expect(")", "Closing parenthesis ')' expected"):
        return
    if not block(scope):
        return
    if lexemeIs("else"):
        advance()
        block(scope)

def whileStatement(scope):
    advance()
    if not expect("(", "Opening parenthesis '(' expected"):
        return
    if not expression():
        return
    if not expect(")", "Closing parenthesis ')' expected"):
        return
    block(scope)

def forStatement(scope):
    advance()
    if not expect("(", "Opening parenthesis '(' expected"):
        return
    if not expression():
        return
    if not expect(";", "Semicolon expected"):
        return
    if not expression():
        return
    if not expect(";", "Semicolon expected"):
        return
    if not expression():
        return
    if not expect(")", "Closing parenthesis ')' expected"):
        return
    if lexemeIs("{"):
        block(scope)
    else:
        statement(scope)

def doStatement(scope):
    advance()
    if not block(scope):
        return
    if not expect("while", "'while' expected after do block"):
        return
    if not expect("(", "Opening parenthesis '(' expected"):
        return
    if not expression():
        return
    if not expect(")", "Closing parenthesis ')' expected"):
        return
    expect(";", "Semicolon expected")


def functionDef(typeName):
    name = current()[1]
    advance()
    symTable.append((name, "Function", "Global", ""))
    scope = name.capitalize()

    if not expect("(", "Opening parenthesis '(' expected"):
        return
    if isType():
        paramType = current()[1]
        advance()
        if isIdentifier():
            symTable.append((current()[1], paramType.capitalize(), scope, ""))
            advance()
    elif not lexemeIs(")"):
        syntaxError("Type specifier expected")
        return
    if not expect(")", "Closing parenthesis ')' expected"):
        return
    block(scope)


def program():
    while current()[0] != "EOF":
        if isType():
            typeName = current()[1]
            advance()
            if lexemeIs("main"):
                functionDef(typeName)
            else:
                initDeclList(typeName, "Global")
        else:
            syntaxError("Type specifier expected", False)


def runParser(fileName):
    global tokens, pos
    errors.clear()
    symTable.clear()
    pos = 0
    tokens = loadTokens(fileName)
    program()

    with open("symbol_table.txt", "w") as f:
        for msg, ln in errors:
            f.write(f"Error: {msg}  (Line {ln})\n")
        if len(errors) > 0:
            f.write("\n")
        f.write(f"{'Lexeme':<12}{'Type':<12}{'Scope':<12}{'Array size'}\n")
        for lexeme, typ, scope, size in symTable:
            f.write(f"{lexeme:<12}{typ:<12}{scope:<12}{size}\n")
    print("Parser done --> Open symbol_table.txt")