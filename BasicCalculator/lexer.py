import ply.lex as lex

#List of reserved words
#List of tokens names - Lista de nombre de tokens
tokens = [

'ID',
'PLUS',
'MINUS',
'DIVIDE',
'MULTIPLY',
'UMINUS',
'ASSIGN',
'LPAREN',
'RPAREN',
'COMMA',
'COLONS',
'LBRACK',
'RBRACK',
'AND',
'OR',
'COMMENT',
'GT',
'LT',
'GE',
'LE',
'NE',
'LARR',
'RARR',
'EQUAL',
'QMARKS',
'INT',
'QUESTION',
'FLOAT'
]

reserved = {
	'int' : 'INT_TYPE',
	'float' : 'FLOAT_TYPE',
	'string': 'STRING',
	'if' : 'IF',
    'begin' : 'BEGIN',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'do' : 'DO',
    'program' : 'PROGRAM',
    'print': 'PRINT',
    'end' : 'END',
    'end_do': 'END_DO',
    'end_if': 'END_IF',
    'elsif' : 'ELSIF',
    'call' : 'CALL',
    'read' : 'READ',
    'loop' : 'LOOP',
    'end_loop' : 'END_LOOP',
    'exit' : 'EXIT',
    'for' : 'FOR',
    'end_for' : 'END_FOR',
    'subroutine' : 'SUBROUTINE'
 }

tokens += reserved.values()

#Regular expressions rules for simple tokens - Reglas de expresiones regulares para nuestros tokens

#Arithmetic operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_ASSIGN = r'\=' 

#Logical operators
t_AND = r'\&'
t_OR = r'\|'
t_GT = r'\>'
t_LT = r'\<'
t_GE = r'\>='
t_LE = r'\<='
t_NE = r'\<>'
t_EQUAL = r'\=='

#Others
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
t_COLONS = r'\:'
t_LBRACK = '{'
t_RBRACK = '}'
t_LARR = r'\['
t_RARR = r'\]'
t_QMARKS = r'\"'
t_QUESTION = r'\?'



t_ignore = r' 	' #Ignore TAB and space

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = 0
    pass

def t_COMMENT(t):
    r'\#.*'
    pass
     # No return value. Token discarded

def t_STRING(t): # finds strings
    r'"\w.+"'
    t.value = t.value[1:-1] # strips the quotation marks of the string
    return t

def t_FLOAT(t):

	r'\d+\.\d+'
	t.value = float(t.value)

	return t

def t_INT(t):

	r'\d+'
	t.value = int(t.value)

	return t

def t_ID(t):

	r'[a-zA-Z][_a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')

	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

