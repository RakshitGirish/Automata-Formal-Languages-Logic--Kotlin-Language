from ply import lex, yacc

# Lexer
tokens = (
    'IDENTIFIER',
    'EQUALS',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'STRING',
    'NUMBER',
)

# Token definitions
t_EQUALS = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'
t_NUMBER = r'\d+'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser rules
def p_list_assignment(p):
    '''
    list_assignment : IDENTIFIER EQUALS list
    '''
    p[0] = {'name': p[1], 'type': 'list', 'value': p[3]}

def p_list(p):
    'list : LBRACKET elements RBRACKET'
    p[0] = p[2]

def p_elements(p):
    '''
    elements : elements COMMA element
             | element
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_element(p):
    '''
    element : NUMBER
            | STRING
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Invalid Syntax at '{p.value}'")
    else:
        print("Invalid Syntax: unexpected end of input")

# Build the parser
parser = yacc.yacc()

# Example usage
while True:
    try:
        s = input('Enter list assignment syntax: ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(f'Valid Syntax: {result}')
