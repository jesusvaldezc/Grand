from lexer import tokens
from CuboSemantico.CuboSemantico import CuboSemantico
import ply.yacc as yacc
import sys


# Cubo Semantico
cuboSemantico = CuboSemantico()

# Pilas para operaciones
PilaOperandos = []
PilaOperadoresLogicos = []
PilaOperadoresAritmeticos = []
# Buffers
Cuadruplos = []
cont = 0

# Variables relaciondas a tabla de variables
tablaVariables = {}
defaultValues = {'int': 9999, 'float': 9999.9999, 'bool': False}
AvailTemp = ['$t1', '$t2', '$t3', '$t4','$t5', '$t6', '$t7', '$t8', '$t9', '$t10']
variableIdQueue = []
currentType = ''
currentOperator = ''

def crearCuadruploNE():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '<>')
		temporal = AvailTemp.pop()
		Cuad = ['<>', OP2,OP1,temporal]
		print("cuad <>")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploLE():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '<=')
		temporal = AvailTemp.pop()
		Cuad = ['<=', OP2,OP1,temporal]
		print("cuad <=")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploGE():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '>=')
		temporal = AvailTemp.pop()
		Cuad = ['>=', OP2,OP1,temporal]
		print("cuad >=")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploEQ():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '==')
		temporal = AvailTemp.pop()
		Cuad = ['==', OP2,OP1,temporal]
		print("cuad ==")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploAsignacion():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global cont
	global tablaVariables
	
	
	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()
	
	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '=')
		Cuad = ['=', OP2,'',OP1]
		print("cuad =")
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploDiv():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '/')
		temporal = AvailTemp.pop()
		Cuad = ['/', OP2,OP1,temporal]
		print("cuad /")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploMul():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '*')
		temporal = AvailTemp.pop()
		Cuad = ['*', OP2,OP1,temporal]
		print("cuad *")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploResta():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '-')
		temporal = AvailTemp.pop()
		Cuad = ['-', OP2,OP1,temporal]
		print("cuad -")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploSuma():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '+')
		temporal = AvailTemp.pop()
		Cuad = ['+', OP2,OP1,temporal]
		print("cuad +")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploLT():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '<')
		temporal = AvailTemp.pop()
		Cuad = ['<', OP2,OP1,temporal]
		print("cuad <")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploGT():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '>')
		temporal = AvailTemp.pop()
		Cuad = ['>', OP2,OP1,temporal]
		print("cuad >")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploAND():
	
	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '&')
		temporal = AvailTemp.pop()
		Cuad = ['&', OP2,OP1,temporal]
		print("cuad &")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def crearCuadruploOR():
	
	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global PilaOperadoresAritmeticos


	OP2 = PilaOperandos.pop()
	OP1 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '|')
		temporal = AvailTemp.pop()
		Cuad = ['|', OP2,OP1,temporal]
		print("cuad |")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)
		cont += 1
		
		if isinstance(OP2, str):
			if OP2[0] == '$':
				AvailTemp.append(OP2)
		if isinstance(OP1, str):
			if OP1[0] == '$':
				AvailTemp.append(OP1)
	else:
		print("OPERADORES INCOMPATIBLES")

def p_program(p):
	'''
	program : PROGRAM ID var_assign subrutinas a END PROGRAM ID

	'''
	print("Programa creado")
	print(Cuadruplos)
	#print(tablaVariables)
	print(cont)
#Declaracion del tipo de variable global

def p_type_definition(p):
	'''
	type_definition : INT_TYPE
					| FLOAT_TYPE
	'''
	global currentType

	currentType = p[1]

def p_var_assign(p):
	'''
	var_assign :  type_definition COLONS COLONS var_local var_dimensiones create_var_table var_assign
				| empty
	'''

def p_var_dimensiones(p):
	'''
	var_dimensiones : LARR constante_entero RARR
					| LARR constante_entero COMMA constante_entero  RARR
					| empty
	'''

#Dimensiones de arreglo aun no esta implementado

def p_create_var_table(p):
	'''
	create_var_table : empty

	'''
	global tablaVariables
	global currentType
	global defaultValues

	while len(variableIdQueue) > 0:
	 currentVar = variableIdQueue.pop()
	 tablaVariables[currentVar] = {'type': currentType, 'value' : defaultValues[currentType]}

def p_var_local(p):
	'''
	var_local : ID COMMA var_local
			      | ID
	'''
	global variableIdQueue
	variableIdQueue.append(p[1])

def p_subrutinas(p):
	'''	
	subrutinas : f_local
				| empty
	'''

def p_f_local(p):
	'''
	f_local : SUBROUTINE ID d END SUBROUTINE ID f_local
			| SUBROUTINE ID d END SUBROUTINE ID
	'''

def p_a(p):
	'''
	a : BEGIN d END

	'''

def p_d(p):
	'''
	d : b d 
	  | b

	'''

def p_b(p):
	'''
	b :   variable_matrix_assign crearCuadruploAsignacion
		| printing_variables
		| if_expression
		| do_loop
		| do_contador
		| do_while_loop
		| call_subroutine
		| reading_variables
	
		
	'''

def p_do_contador(p):
	'''
	do_contador : DO ID COMMA ID COMMA variable_matrix_assign d END_DO
				| DO constante_entero COMMA constante_entero COMMA variable_matrix_assign d END_DO
	'''

def p_reading_variables(p):
	'''
	reading_variables : READ ID
	'''

def p_do_loop(p):
	'''
	do_loop : DO d END_DO


	'''

def p_do_while_loop(p):
	'''

	do_while_loop : DO WHILE expression_logic d END_DO


	'''

def p_call_subroutine(p):
	
	'''
	call_subroutine : CALL ID

	'''

def p_if_expression(p):
	'''
	if_expression : IF expression_logic THEN  if_expression_local  if_expression_local2 ELSE if_expression_local  END_IF
				  | IF expression_logic THEN  if_expression_local  END_IF 
	
	'''

def p_if_expression_local(p):
	'''
	if_expression_local : d	 
						 | empty
	'''

def p_if_expression_local2(p):
	'''
	if_expression_local2 : if_expression_local2  ELSIF expression_logic  THEN if_expression_local 	 
						 | empty
	'''
def p_printing_variables(p):
	'''
	printing_variables : PRINT LPAREN expression_arith RPAREN
					   | PRINT LPAREN STRING RPAREN
	
	'''

def p_variable_matrix_assign(p):
	'''
	variable_matrix_assign :  ID ASSIGN expression_arith 
	  						| ID LPAREN expression_arith RPAREN ASSIGN expression_arith crearCuadruploAsignacion
	  						| ID LPAREN expression_arith COMMA expression_arith RPAREN ASSIGN expression_arith crearCuadruploAsignacion

	'''
	global PilaOperandos
	PilaOperandos.append(p[1])

	
#--------------------------------definicion expresionles aritmeticas
def p_expression_arith(p):
	'''
	expression_arith :                 expression_arith PLUS c crearCuadruploSuma
					 				 | expression_arith MINUS c crearCuadruploResta
									 | c 
							
	'''

def p_c(p):

	'''
	c : c MULTIPLY te crearCuadruploMul
		| c DIVIDE te crearCuadruploDiv
		| te 
	'''

def p_te(p):
	'''
	te : ID 
	  | constante_entero
	  | constante_flotante
	  | ID LPAREN expression_arith RPAREN
	  | ID LPAREN expression_arith COMMA expression_arith RPAREN
	  | LPAREN expression_arith RPAREN

	'''	

	global PilaOperandos
	PilaOperandos.append(p[1])

def p_crearCuadruploSuma(p):
	'''
	crearCuadruploSuma : empty

	'''

	crearCuadruploSuma()


def p_crearCuadruploResta(p):
	'''
	crearCuadruploResta : empty

	'''

	crearCuadruploResta()

def p_crearCuadruploMul(p):
	'''
	crearCuadruploMul : empty

	'''

	crearCuadruploMul()

def p_crearCuadruploDiv(p):
	'''
	crearCuadruploDiv : empty

	'''

	crearCuadruploDiv()

def p_crearCuadruploAsignacion(p):
	'''
	crearCuadruploAsignacion : empty

	'''
	crearCuadruploAsignacion()

	global PilaOperandos

	PilaOperandos.append(p[1]) 

def p_expression_logic(p):
	'''
	expression_logic : expression_logic OR g
					 | g				 
			
	'''
	if len(p) > 2:
		PilaOperadoresLogicos.append(p[2])
	
def p_g(p):

	'''
	g : g AND ge 
	  | ge

	'''
	if len(p) > 2:
		PilaOperadoresLogicos.append(p[2])
		
		

def p_ge(p):

	'''
	ge : ID GT ID
	   | ID LT ID
	   | ID GE ID
	   | ID LE ID
	   | ID NE ID
	   | ID EQUAL ID
	   | LPAREN expression_logic RPAREN
	
	'''

	global PilaOperandos
	
	if p[1] is not '(' and p[3] is not ')':
		PilaOperandos.append(p[1]) 
		PilaOperandos.append(p[3])
			

def p_constante_entero(p):
	'''
	constante_entero : INT 

	'''
	global tablaVariables

	tablaVariables[p[1]] = {'type': 'int', 'value': p[1]}
	p[0] = p[1]

def p_constante_flotante(p):
	'''
	constante_flotante : FLOAT
	
	'''
	global tablaVariables

	tablaVariables[p[1]] = {'type': 'float', 'value': p[1]}
	p[0] = p[1]

def p_error(p):
	print("Syntax error at '%s'" % p)

def p_empty(p):
	'''
	empty : 
	'''

parser = yacc.yacc()

print("Leyendo de prueba3: ")
fileName = "prueba3.txt"

file = open(fileName, 'r')
code = file.read()
'''

lexer.input(code)

while  True:
	tok = lexer.token()
	if not tok:
		break
	print(tok)
'''
print(code)
parser.parse(code)


