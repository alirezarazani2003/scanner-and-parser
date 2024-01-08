TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_NUMBER = "NUMBER"
TOKEN_RESERVED_WORD = "RESERVED_WORD"
TOKEN_SYMBOL = "SYMBOL"
TOKEN_STRING = "STRING"
TOKEN_META_STATEMENT = "META_STATEMENT"

def program(tokens):
    data_decls(tokens)
    func_list(tokens)

def func_list(tokens):
    while len(tokens) > 0:
        func(tokens)
        func_list(tokens)

def func(tokens):
    func_decl(tokens)
    if tokens[0][1] == ";":
        tokens.pop(0)
    else:
        tokens.pop(0)
        data_decls(tokens)
        statements(tokens)
        if len(tokens) > 0:
            tokens.pop(0)
        else:
            return

def func_decl(tokens):
    if len(tokens) < 3:
        print("Error: Insufficient tokens for function declaration")
        return
    type_name(tokens)
    tokens.pop(0)
    tokens.pop(0)
    parameter_list(tokens)
    tokens.pop(0)

def type_name(tokens):
    if tokens[0][0] == TOKEN_RESERVED_WORD:
        tokens.pop(0)
    else:
        print(f"Expected type name, found {tokens[0][1]} at line {tokens[0][2]+1}")
        tokens.pop(0)


def parameter_list(tokens):
    if tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "void":
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_IDENTIFIER:
        tokens.pop(0)
        tokens.pop(0)
        parameter_list(tokens)
    else:
        print(f"Expected parameter list, found {tokens[0][1]} at line {tokens[0][2]+1}")


def data_decls(tokens):
    if len(tokens) > 0 and tokens[0][0] == TOKEN_RESERVED_WORD:
        type_name(tokens)
        id_list(tokens)
        tokens.pop(0)
        data_decls(tokens)


def id_list(tokens):
    if tokens[0][0] == TOKEN_IDENTIFIER:
        tokens.pop(0)
    else:
        print(f"Expected identifier, found {tokens[0][1]} at line {tokens[0][2]+1}")
        tokens.pop(0)
    if tokens[0][1] == ",":
        tokens.pop(0)
        id_list(tokens)


def statements(tokens):
    if len(tokens) > 0:
        statement(tokens)
        statements(tokens)


def statement(tokens):
    if tokens[0][0] == TOKEN_IDENTIFIER:
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_IDENTIFIER and tokens[1][1] == "(":
        tokens.pop(0)
        tokens.pop(0)
        expr_list(tokens)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "if":
        tokens.pop(0)
        tokens.pop(0)
        condition_expression(tokens)
        tokens.pop(0)
        block_statements(tokens)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "while":
        tokens.pop(0)
        tokens.pop(0)
        condition_expression(tokens)
        tokens.pop(0)
        block_statements(tokens)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "return":
        tokens.pop(0)
        if tokens[0][0] != TOKEN_SYMBOL or tokens[0][1] != ";":
            expression(tokens)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "break":
        tokens.pop(0)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "continue":
        tokens.pop(0)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "read":
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "write":
        tokens.pop(0)
        tokens.pop(0)
        expression(tokens)
        tokens.pop(0)
    elif tokens[0][0] == TOKEN_RESERVED_WORD and tokens[0][1] == "print":
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
    else:
        print(f"Unrecognized statement at line {tokens[0][2]+1}")
        tokens.pop(0)

def expr_list(tokens):
    if len(tokens) > 0:
        expression(tokens)
        if tokens[0][1] == ",":
            tokens.pop(0)
            expr_list(tokens)

def condition_expression(tokens):
    condition(tokens)
    if tokens[0][0] == TOKEN_SYMBOL and (tokens[0][1] == "&&" or tokens[0][1] == "||"):
        tokens.pop(0)
        condition_op(tokens)
        condition(tokens)

def condition_op(tokens):
    if tokens[0][0] == TOKEN_SYMBOL and (tokens[0][1] == "&&" or tokens[0][1] == "||"):
        tokens.pop(0)
    else:
        print(f"Expected condition operator, found {tokens[0][1]} at line {tokens[0][2]+1}")


def condition(tokens):
    expression(tokens)
    comparison_op(tokens)
    expression(tokens)


def comparison_op(tokens):
    if tokens[0][0] == TOKEN_SYMBOL and (tokens[0][1] == "==" or tokens[0][1] == "!=" or tokens[0][1] == ">" or tokens[0][1] == ">=" or tokens[0][1] == "<" or tokens[0][1] == "<="):
        tokens.pop(0)
    else:
        print(f"Expected comparison operator, found {tokens[0][1]} at line {tokens[0][2]+1}")

def block_statements(tokens):
    if tokens[0][1] == "{":
        tokens.pop(0)
        statements(tokens)
        tokens.pop(0)
    else:
        print(f"Expected block statements, found {tokens[0][1]} at line {tokens[0][2]+1}")


def expression(tokens):
    term(tokens)
    if tokens[0][0] == TOKEN_SYMBOL and (tokens[0][1] == "+" or tokens[0][1] == "-"):
        tokens.pop(0)
        addop(tokens)
        term(tokens)

def addop(tokens):
    if tokens[0][0] == TOKEN_SYMBOL and (tokens[0][1] == "+" or tokens[0][1] == "-"):
        tokens.pop(0)
    else:
        print(f"Expected add operator, found {tokens[0][1]} at line {tokens[0][2]+1}")


def term(tokens):
    pass


def syntax_analyzer(tokens):
    stack = ['$', '<start>']  # Initialize stack with end marker and start symbol
    table = {
        '<start>': {'<reserved_word>': ['<declaration>', '<start>'],
                    '<identifier>': ['<statement>', '<start>']},
        '<declaration>': {'<reserved_word>': ['<reserved_word>', '<declaration>'],
                          '<identifier>': ['<identifier>', '<declaration>'],
                          '': []},
        '<statement>': {'<reserved_word>': ['<reserved_word>', '<statement>'],
                        '<identifier>': ['<identifier>', '<statement>'],
                        '': []},
        '<reserved_word>': {'int': ['int'],
                            'void': ['void'],
                            # Add more reserved words and their productions
                            },
        '<identifier>': {'<identifier_name>': ['<identifier_name>'],
                         # Add more identifier productions
                         },
        # Add more grammar rules and their productions
    }
    lent = len(tokens)
    while len(stack) > 0:
        top = stack[-1]
        for i in range(lent):
            token = tokens[i]

            if top == token:
                stack.pop()
                tokens.pop(0)
            elif top in table and token in table[top]:
                stack.pop()
                production = table[top][token]
                stack.extend(production[::-1])  # Push production's elements to the stack in reverse order
            else:
                raise SyntaxError(f"Invalid token: {token}")

    if len(tokens) == 0:
        print("Syntax analysis successful")
    else:
        print("Syntax analysis failed")

def syntax_analyzer2(tokens):
    stack = ['$', '<start>']  # Initialize stack with end marker and start symbol
    index = 0  # Token index
    
    # Define the parsing table
    table = {
        '<start>': ['<reserved word>', '<symbol>', '<string>', '<meta statement>'],
        '<reserved word>': ['int', 'void', 'if', 'while', 'return', 'read', 'write', 'print', 'continue', 'break', 'binary', 'decimal'],
        '<symbol>': ["( )", "{ }", "[ ]", ",", ";", "+", "-", "*", "/", "==", "!=", ">", ">=", "<", "<=", "=", "&&", "||"],
        '<string>': ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "E", "S", "T", "U", "V", "W", "X", "Y", "Z", "_"],
        '<meta statement>': ["#" or "//"]
    }
    
    while stack:
        top = stack[-1]  # Get the top of the stack
        
        if top == '$':  # If stack is empty
            if tokens[index][0] == '$':  # If all tokens have been consumed
                print("Syntax analysis successful!")
                return True
            else:
                print("Syntax error: Unexpected token")
                return False
        
        if top in table:  # If top is a non-terminal symbol
            if tokens[index][0] in table[top]:  # If there is a valid production
                stack.pop()  # Pop the non-terminal symbol
                production = table[top][tokens[index][0]]  # Get the production
                for symbol in reversed(production):
                    stack.append(symbol)  # Push the production symbols in reverse order
            else:
                print("Syntax error: Invalid token")
                return False
        
        elif top == tokens[index][0]:  # If top matches the current token
            stack.pop()  # Pop the token
            index += 1  # Move to the next token
        
        else:
            print("Syntax error: Unexpected token")
            return False
    
    print("Syntax error: Unexpected end of stack")
    return False

