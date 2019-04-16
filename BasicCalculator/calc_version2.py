import ply.lex as lex
import ply.yacc as yacc
import sys

#List of reserved words


#List of tokens names - Lista de nombre de tokens
tokens = [

'INT',
'FLOAT',
'NAME',
'PLUS',
'MINUS',
'DIVIDE',
'MULTIPLY',
'EQUALS',
'AND',
'OR',
'LPAREN',
'RPAREN',
'COMMA',
'SEMI',
'DOT',
'TRUE',
'FALSE',
 'LBRACK',
 'RBRACK',
'POWER'

]

reserved = {

	'int' : 'INT_TYPE',
	'float' : 'FLOAT_TYPE',
	'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'program' : 'PROGRAM',
    'var' : 'VAR'

 }

tokens += reserved.values()

#Regular expressions rules for simple tokens - Reglas de expresiones regulares para nuestros tokens


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\:=' 
t_AND = r'\&'
t_OR = r'\|'
t_POWER = r'\ç'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMI = r';'
t_DOT = r'\.'
t_LBRACK = '{'
t_RBRACK = '}'
t_ignore = r' 	' #Ignore TAB and space

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = 0
    pass

def t_FLOAT(t):

	r'\d+\.\d+'
	t.value = float(t.value)

	return t

def t_INT(t):

	r'\d+'
	t.value = int(t.value)

	return t

def t_NAME(t):

	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'NAME')

	return t

def t_TRUE(t):
    'true'
    t.value = True

    return t

def t_FALSE(t):

    'false'
    t.value = False
    return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

#Nos muestra el orden el cual la operacion se atendera de menor a mayor

precedence = (

	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE'),
	('left', 'POWER')
	)

def p_program(p):
	'''
	program : PROGRAM NAME SEMI var_assign b DOT

	'''
	print("Programa creado")

def p_b(p):

	'''
	b : LBRACK statements RBRACK

	'''

def p_var_assign(p):
	'''
	var_assign : VAR  EQUALS type SEMI 
				| empty
	'''
	p[0] = (':=', p[2], p[4])

def p_type(p):
	'''
	type : INT_TYPE 
		| FLOAT_TYPE

	'''

def p_statements(p):
	'''
	statements :  NAME EQUALS expression
				| b

	'''
def p_expression_var(p):
	'''
	expression :	NAME
				
	'''
	p[0] = ('var', p[1])

def p_expression(p):
	'''
	expression : expression PLUS expression SEMI

	'''
	if p[2] == '+' : p[0] = p[1] + p[3]
	print(p[0])

def p_expression_int_float(p):
	'''
	expression : INT 
				| FLOAT

	'''
	p[0] = p[1]



def p_empty(p):
	'''
	empty : 

	'''
	p[0] = None

parser = yacc.yacc()

while True:
	try:
		s = input('>> ')
	except EOFError:
		break
	parser.parse(s)



