from ply import lex, yacc

# Lexer
tokens = (
    'IDENTIFIER',
    'EQUALS',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'STRING',
    'NUMBER',
)

# Token definitions
t_EQUALS = r'='
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove surrounding quotes
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

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
def p_tuple_assignment(p):
    '''
    tuple_assignment : IDENTIFIER EQUALS tuple
    '''
    p[0] = {'name': p[1], 'type': 'tuple', 'value': p[3]}

def p_tuple(p):
    'tuple : LPAREN elements RPAREN'
    p[0] = {'type': 'tuple', 'elements': p[2]}

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
        s = input('Enter tuple assignment syntax: ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    if result:
        print(f'Valid Syntax: {result}')
