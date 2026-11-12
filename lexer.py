from tokens import Keywords, Numbers , Operators


def tokenize(s_code):
    tkn=[]
    i=0
    lineNo = 1
    length = len(s_code)

    while i < length:
        ch = s_code[i]
        if ch.isalpha():
            word = ""
            while i < length and (s_code[i] == "_" or s_code[i].isdigit() or s_code[i].isalpha()):
                word = word + s_code[i]
                i+=1
            if word.lower() in Keywords:
                tkn.append(("Keyword",word,lineNo))
            else:
                tkn.append(("Identifier",word,lineNo))

        elif ch in Numbers:
            num=""
            while i < length and  s_code[i] in Numbers :
                num = num + s_code[i]
                i+=1
            
            if len(num) > 0 :
                tkn.append(("Number",num,lineNo))


        elif ch == "/" and i + 1 < length and s_code[i+1] == "*":
            startLine = lineNo
            i += 2
            closed = False
            while i < length:
                if s_code[i] == "*" and i + 1 < length and s_code[i+1] == "/":
                    closed = True
                    i += 2
                    break
                if s_code[i] == "\n":
                    lineNo += 1
                i += 1
            if not closed:
                tkn.append(("Error","unclosed comment", startLine))

        elif ch == "=" and i + 1 < length and s_code[i+1] == "=":
            tkn.append(("Operator","==",lineNo))
            i+=2

        elif ch in Operators:
            tkn.append(("Operator",ch,lineNo))
            i+=1

        elif ch == '"':
            text = '"'
            i += 1
            closed = False
            while i < length and s_code[i] != "\n":
                text = text + s_code[i]
                if s_code[i] == '"':
                    closed = True
                    i += 1
                    break
                i += 1
            if closed:
                tkn.append(("String", text, lineNo))
            else:
                tkn.append(("Error", "String constant exceeds line", lineNo))
                while i < length and s_code[i] != "\n":
                    i += 1

        elif ch == "'":
            content = ""
            i += 1
            while i < length and s_code[i] != "'" and s_code[i] != "\n":
                content = content + s_code[i]
                i += 1
            closed = i < length and s_code[i] == "'"
            if closed and len(content) == 1:
                tkn.append(("Char", "'" + content + "'", lineNo))
                i += 1
            else:
                if len(content) > 1:
                    tkn.append(("Error", "Char constant too long", lineNo))
                else:
                    tkn.append(("Error", "Invalid char constant", lineNo))
                while i < length and s_code[i] != "\n":
                    i += 1

        elif ch == "\n":
            lineNo +=1  
            i+=1

        elif ch == " " or ch == "\t" or ch == "\r":
            i += 1
        
        else:
            tkn.append(("Error", "symbol not defined " + ch, lineNo))
            while i < length and s_code[i] != "\n":
                i+=1

    # tkn.append(("Keyword","int",1))
    return tkn