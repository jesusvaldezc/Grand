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
'POWER'

]

reserved = {

	'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR'

 }

tokens += reserved.values()

#Regular expressions rules for simple tokens - Reglas de expresiones regulares para nuestros tokens


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\->' 
t_AND = r'\&'
t_OR = r'\|'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
t_SEMI = r'\;'
t_ignore = r' 	' #Ignore TAB and space


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

def t_error(t):

	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()



#Nos muestra el orden el cual la operacion se atendera de menor a mayor

precedence = (

	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE'),
	('left', 'POWER'),
	('right', 'UMINUS'),
	)

def p_calc(p):
	'''
	calc : expression
		| var_assign
		| empty	
	'''
	print(run(p[1]))

#Asigna una expression a una variable
def p_var_assign(p):
	'''
	var_assign : NAME EQUALS expression SEMI

	'''
	p[0] = ('->', p[1], p[3])

def p_empty(p):
	'''
	empty :
	'''
	p[0] = None

#Permite tener representacion negativa del numero
def p_expression_uminus(p):
        '''
        expression : MINUS expression %prec UMINUS

        '''
        p[0] = -p[2]


#Define una expression para expresiones numericas
def p_expression_int_float(p):
	'''
	expression :	INT
				| FLOAT
	'''
	p[0] = p[1]

#permite que una expression se use con una variable, permite 1+a
def p_expression_var(p):
	'''
	expression :	NAME
				
	'''
	p[0] = ('var', p[1])

def p_error(p):
	print("Syntax error found")

#Define las expresiones logicas y numericas

def p_expression(p):
	'''
	expression  : expression MULTIPLY expression
				| expression DIVIDE expression
				| expression PLUS expression
				| expression MINUS expression
				| expression POWER expression

				
	'''
	p[0] = (p[2], p[1], p[3])


#Diccionario del codigo
env = {}

#Manda a llamar el proceso de forma recursiva que permite realizar las operaciones

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

		elif p[0] == '->':
			env[p[1]] = run(p[2])

		elif p[0] == '^':
			return run(p[1]) ** run(p[2])

		elif p[0] == 'var':
			if p[1] not in env:
				return ('%s'' is a undeclared variable' % p[1])
			return env[p[1]]
	else:

		return p

#lexer.input(data)

#while  True:
#	tok = lexer.token()
#	if not tok:
#		break
#	print(tok)

parser = yacc.yacc()

while True:
	try:
		s = input('>> ')
	except EOFError:
		break
	parser.parse(s)

'''
a := int;

env = {}

env[NAME] = ('int', 99999)

a = 1;

env.a[1] = 1;

{
	a: ('int', 1)
}
'''