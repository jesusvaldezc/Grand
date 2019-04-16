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
'COLONS',
'LBRACK',
'RBRACK',
'POWER'

]

reserved = {

	'int' : 'INT_TYPE',
	'float' : 'FLOAT_TYPE',
	'if' : 'IF',
    'begin' : 'BEGIN',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'program' : 'PROGRAM',
    'var' : 'VAR',
    'print': 'PRINT',
    'end' : 'END'

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
t_COLONS = r'\:'
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
	program : PROGRAM NAME var_assign b END PROGRAM NAME

	'''
	print("Programa creado")

def p_b(p):

	'''
	b : BEGIN c END

	'''

def p_c(p):

	'''
	c : statements c
	| statements

	'''

def p_var_assign(p):
	'''
	var_assign : type a
				| empty
	'''

def p_a(p):
	'''
	a : COLONS COLONS d

	'''
	p[0] = ('::', p[1], p[3])


def p_d(p):
	'''
	d : NAME COMMA d
		| NAME 

	'''

def p_type(p):
	'''
	type : INT_TYPE 
		| FLOAT_TYPE


	'''

def p_statements(p):
	'''
	statements :  NAME EQUALS expression
	
	'''

	p[0] = (':=', p[1],p[3])

	run(p[0]) #permite la asignacion

def p_expression_var(p):
	'''
	expression :	NAME
				
	'''
	p[0] = ('var', p[1])

def p_expression(p):
	'''
	expression :  expression PLUS expression
				| expression MINUS expression
				| expression MULTIPLY expression
				| expression DIVIDE expression
				| expression POWER expression

	'''
	p[0] = (p[2],p[1],p[3])

	run(p[0]) #Resultado completo

def p_expression_int_float(p):
	'''
	expression : INT
			| FLOAT 
			
	'''
	p[0] = p[1]

def p_print(p):
	'''
	statements : PRINT LPAREN expression RPAREN

	'''

	p[0] = print(run(p[3]))
	
def p_error(p):
	print("Syntax error at '%s'" % p)

def p_empty(p):
	'''
	empty : 

	'''
	p[0] = None

env = {}

def run(p):
	global env
	if type(p) == tuple:
        
		if p[0] == '+':
			return run(p[1]) + run(p[2])
        
		elif p[0] == '-':
			return run(p[1]) - run(p[2])
        
		elif	p[0] == '*':
			return run(p[1]) * run(p[2])
        
		elif p[0] == '/':
			return run(p[1]) / run(p[2])
        
		elif p[0] == 'ç':
			return run(p[1]) ** run(p[2])
        
		elif p[0] == '&':
			return run(p[1]) and run(p[2])
        
		elif p[0] == ':=':
			env[p[1]] = run(p[2])
        
		elif p[0] == 'var':
            
			if p[1] not in env:
				return ('%s'' is a undeclared variable' % p[1])
			return env[p[1]]
	else:
		return p


parser = yacc.yacc()

print("Ruta del archivo de prueba: ")
fileName = input()

file = open(fileName, 'r')
code = file.read()

print(code)

#while True:
#	try:
#		s = input('>> ')
#	except EOFError:
#		break
parser.parse(code)



