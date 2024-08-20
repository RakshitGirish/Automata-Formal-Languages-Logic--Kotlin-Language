from ply import lex, yacc

# Lexer
tokens = (
    'IDENTIFIER',
    'EQUALS',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'STRING',
    'NUMBER',
)

# Token definitions
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_NUMBER = r'\d+'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser rules
def p_set_assignment(p):
    '''
    set_assignment : IDENTIFIER EQUALS set
    '''
    p[0] = {'name': p[1], 'type': 'set', 'value': p[3]}

def p_set(p):
    'set : LBRACE elements RBRACE'
    p[0] = {'type': 'set', 'elements': p[2]}

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
    print("Invalid Syntax")

# Build the parser
parser = yacc.yacc()

# Example usage
while True:
    try:
        s = input('Enter set assignment syntax: ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    if result:
        print(f'Valid Syntax: {result}')
