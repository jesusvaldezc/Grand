import ply.lex as lex
import ply.yacc as yacc
import sys

#List of reserved words


#List of tokens names - Lista de nombre de tokens
tokens = [

'HOLA',
'COMMA',
'QUE',
'TAL'

]

t_HOLA = r'HOLA'
t_COMMA = r'\,'
t_QUE = r'QUE'
t_TAL = r'TAL'
t_ignore = r' 	'

def t_error(t):

	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

lexer.input("HOLA ,QUE TAL")

while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok)


def p_calc(p):
	'''
		calc : 	X QUE TAL
			
	'''

# S - A QUE TAL
# A - HOLA
# A - HOLA,

def p_X(p):
	'''
	  X : HOLA 
		| X COMMA HOLA

	'''

def p_empty(p):
	'''
		empty :

	'''
	#return empty

parser = yacc.yacc()

while True:
	try:
		s = input('Teclea frase >> ')
	except EOFError:
		break
	parser.parse(s)

