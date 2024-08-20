from ply import lex, yacc

# Lexer
tokens = (
    'ID',
    'EQUALS',
    'LCPAREN',
    'COLON',
    'COMMA',
    'RCPAREN',
)

# Token definitions
t_LCPAREN = r'\{'
t_RCPAREN = r'\}'
t_COMMA = r','
t_EQUALS = r'='
t_COLON = r':'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*|\d+'
    return t

t_ignore = ' \t\''

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser rules
def p_dictionary(p):
    '''
    dictionary : LCPAREN key_value_pairs RCPAREN
               | ID EQUALS LCPAREN key_value_pairs RCPAREN
    '''
    if len(p) == 4:
        p[0] = {'type': 'dictionary', 'value': p[2]}
    else:
        p[0] = {'name': p[1], 'type': 'dictionary', 'value': p[4]}
    print(f"Valid syntax for dictionary: {p[0]}")

def p_key_value_pairs(p):
    '''
    key_value_pairs : key_value_pairs COMMA key_value_pair
                   | key_value_pair
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_key_value_pair(p):
    '''
    key_value_pair : ID COLON ID
    '''
    p[0] = (p[1], p[3])

# Error handling rule
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Example usage
input_text = "a={'ok':'bye','hi':3}"
lexer.input(input_text)
parsed_result = parser.parse(input_text)

if parsed_result:
    print(f"Parsed result: {parsed_result}")
