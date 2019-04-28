from lexer import tokens
from CuboSemantico.CuboSemantico import CuboSemantico
import ply.yacc as yacc
import sys
import json

# Cubo Semantico
cuboSemantico = CuboSemantico()

# Pilas para operaciones
PilaOperandos = []
PiladeSaltos = []
PiladeExits = [] 

# Buffers
Cuadruplos = []
cont = 0
marca = 200
forID = 0

# Variables relaciondas a tabla de variables
tablaVariables = {}
defaultValues = {'int': 0, 'float': 0.0, 'bool': False}
AvailTemp = ['$t1', '$t2', '$t3', '$t4','$t5', '$t6', '$t7', '$t8', '$t9', '$t10']
variableIdQueue = []
currentType = ''
currentOperator = ''
stringOutput = ''

def Rellenar(direccion1, direccion2):
	
	global Cuadruplos

	Cuad = Cuadruplos[direccion1]
	tipoGoto = Cuad[0]
	if (tipoGoto == 'goto' or tipoGoto == 'read'):
		CuadNuevo = (Cuad[0],direccion2,'','')
		Cuadruplos[direccion1] = CuadNuevo
	else:
		CuadNuevo = (Cuad[0], Cuad[1], direccion2, '')
		Cuadruplos[direccion1] = CuadNuevo
	
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
		Cuad = ['<>', OP1,OP2,temporal]
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
		Cuad = ['<=', OP1,OP2,temporal]
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

def crearCuadruploLE_FOR():

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
		Cuad = ['<=', OP1,OP2,temporal]
		print("cuad <= FOR")
		PilaOperandos.append(temporal)
		tablaVariables[temporal] = {'type': resultType, 'value': defaultValues[resultType]}
		Cuadruplos.append(Cuad)

		PiladeSaltos.append(cont)
		cont += 1

		PilaOperandos.insert(0,OP1)
		
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
		Cuad = ['>=', OP1,OP2,temporal]
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
		Cuad = ['==', OP1,OP2,temporal]
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
		Cuad = ['=', OP1,'',OP2]
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

def crearCuadruploAsignacionFOR():

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
		print("cuad = FOR")
		Cuadruplos.append(Cuad)
		cont += 1

		PilaOperandos.append(OP1)
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
		Cuad = ['/', OP1,OP2,temporal]
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
		Cuad = ['*', OP1,OP2,temporal]
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
		Cuad = ['-', OP1,OP2,temporal]
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
		Cuad = ['+', OP1,OP2,temporal]
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

def crearCuadruploSumaFOR():

	global PilaOperandos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	tablaVariables[1] = {'type': 'int', 'value' : 1}

	OP2 = PilaOperandos.pop(0)
	OP1 = 1

	OP2Type = tablaVariables.get(OP2)
	OP1Type = tablaVariables.get(OP1)
	
	if OP2Type is not None and OP1Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], OP1Type['type'], '+')
		Cuad = ['+', OP1,OP2,OP2]
		print("cuad + FOR")
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
		Cuad = ['<', OP1,OP2,temporal]
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
		Cuad = ['>', OP1,OP2,temporal]
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
		Cuad = ['&', OP1,OP2,temporal]
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
		Cuad = ['|', OP1,OP2,temporal]
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

def crearCuadruploGoToF():
	
	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	OP2 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	
	if OP2Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], 'bool', '|')
		Cuad = ['gotoF', OP2,'','']
		print("gotoF ")
		Cuadruplos.append(Cuad)
		cont += 1
		
	else:
		print("OPERACION INCOMPATIBLE")

def crearCuadruploGoTo():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	Cuad = ['goto','','','']
	print("goto")
	Cuadruplos.append(Cuad)
	cont += 1

def crearCuadruploGoToFOR():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	direccion = PiladeSaltos.pop()

	Cuad = ['goto',direccion,'','']
	print("goto FOR")
	Cuadruplos.append(Cuad)
	cont += 1
	Rellenar(direccion + 1, cont)

def crearCuadruploGoToDoExit():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	direccion = PiladeSaltos.pop()

	Cuad = ['goto',direccion,'','']
	print("gotoDoExit")
	Cuadruplos.append(Cuad)
	cont += 1

def crearCuadruploGoToV():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	OP2 = PilaOperandos.pop()

	OP2Type = tablaVariables.get(OP2)
	
	if OP2Type is not None:
		resultType = cuboSemantico.validarTipoPorOperacion(OP2Type['type'], 'bool', '|')
		Cuad = ['gotoV', OP2,'','']
		print("gotoV ")
		Cuadruplos.append(Cuad)
		cont += 1
		
	else:
		print("OPERACION INCOMPATIBLE")

def crearCuadruploGoToDoExit():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	direccion = PiladeSaltos.pop()

	Cuad = ['goto',direccion,'','']
	print("gotoDoExit")
	Cuadruplos.append(Cuad)
	cont += 1

def crearCuadruploREAD():
		
		global PilaOperandos
		global PiladeSaltos
		global AvailTemp
		global Cuadruplos
		global tablaVariables
		global cont


		Cuad = ['read','','','']
		print("cuad READ")

		Cuadruplos.append(Cuad)
		cont += 1

def crearCuadruploSTRING():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont
	global stringOutput

	Cuad = ['outputS',stringOutput,'','']
	print("cuad OUTPUT String")
	Cuadruplos.append(Cuad)
	cont += 1	

def crearCuadruploOutput():

	global PilaOperandos
	global PiladeSaltos
	global AvailTemp
	global Cuadruplos
	global tablaVariables
	global cont

	operandoImprimir = PilaOperandos.pop()
	Cuad = ['outputV', operandoImprimir, '', '']
	print("cuad OUTPUT Variable")
	Cuadruplos.append(Cuad)
	cont += 1

def p_program(p):

	'''
	program : PROGRAM ID primerCuad var_assign subrutinas rellenaCuad a END PROGRAM ID

	'''
	print("Programa creado")

	for x in range(len(Cuadruplos)): 
		print(Cuadruplos[x]) 
		
	#print(tablaVariables)
	print(cont)
	#print(PiladeSaltos)
	#print(PilaOperandos)

#Declaracion del tipo de variable global

def p_primerCuad(p):
	'''
	primerCuad : empty
	'''

	crearCuadruploGoTo()

def p_rellenaCuad(p):
	'''
	rellenaCuad : empty
	'''
	global cont

	Rellenar(0, cont)

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
	d : b
	  | b d

	'''

def p_b(p):
	'''
	b :   variable_matrix_assign
		| printing_variables
		| if_expression
		| do_loops
		| call_subroutine
		| reading_variables
		| EXIT paso4DoExit
		
	'''

def p_do_loops(p):
	'''
	do_loops : FOR paso1FOR ASSIGN expression_arith paso2FOR COMMA expression_arith paso3FOR DO d paso4FOR END_FOR
			| DO constante_entero COMMA constante_entero COMMA variable_matrix_assign d END_DO
			| DO paso1DO LOOP d WHILE expression_logic END_DO paso2DO
			| LOOP paso1DoExit d END_LOOP paso2DoExit paso3DoExit

	'''

def p_paso1FOR(p):
	'''
	paso1FOR : ID

	'''

	global PilaOperandos
	PilaOperandos.append(p[1])

def p_paso2FOR(p):
	'''
	paso2FOR : empty

	'''

	crearCuadruploAsignacionFOR()

def p_paso3FOR(p):
	'''
	paso3FOR : empty

	'''
	global cont

	crearCuadruploLE_FOR()

	crearCuadruploGoToF()

def p_paso4FOR(p):
	'''
	paso4FOR : empty

	'''

	crearCuadruploSumaFOR()

	crearCuadruploGoToFOR()

def p_reading_variables(p):
	'''
	reading_variables : READ idrepInput
	'''

def p_idrepInput(p):
	'''
	idrepInput : idInput
				| idInput COMMA idrepInput			

	'''

def p_idInput(p):
	'''
	idInput : ID

	'''
	global cont
	crearCuadruploREAD()
	local = p[1]
	Rellenar(cont -1, local)


def p_call_subroutine(p):
	'''
	call_subroutine : CALL ID

	'''
def p_if_expression(p):
	'''
	if_expression : IF expression_logic paso1IF THEN  if_expression_local if_expression_local2 paso2IF ELSE if_expression_local paso3IF END_IF
				  | IF expression_logic paso1IF THEN if_expression_local paso3IF END_IF
	
	'''

def p_if_expression_local(p):
	'''
	if_expression_local : d	 
						 | empty
	'''

def p_if_expression_local2(p):
	'''
	if_expression_local2 : ELSIF expression_logic THEN if_expression_local if_expression_local2 
						 | empty
	'''

def p_printing_variables(p):
	'''

	printing_variables : PRINT Output
					
	'''

def p_Output(p):
	'''
	Output : idOut
		  | LPAREN StringOut RPAREN

	'''
	global stringOutput

	if p[1] == '(':
		crearCuadruploSTRING()
		stringOutput = ''

def p_StringOut(p):
    '''
	StringOut : empty
			  | ID StringOut
			  | constante_entero StringOut
			  | constante_flotante StringOut   
			  | COLONS StringOut
			  | COMMA StringOut 
			  | QUESTION StringOut
				
		'''
    global stringOutput

    if p[1] != None:
        stringOutput = str(p[1]) + ' ' + stringOutput

def p_idOut(p):
	'''
	idOut : ID

	'''
	global PilaOperandos

	PilaOperandos.append(p[1])

	crearCuadruploOutput()

	

def p_variable_matrix_assign(p):
	'''
	variable_matrix_assign :  ID ASSIGN expression_arith
	  						| ID LPAREN expression_arith RPAREN ASSIGN expression_arith 
	  						| ID LPAREN expression_arith COMMA expression_arith RPAREN ASSIGN expression_arith

	'''
	global PilaOperandos
	PilaOperandos.append(p[1])

	if p[2] is '=':
		crearCuadruploAsignacion()
		
def p_expression_arith(p):
	'''
	expression_arith :                 expression_arith PLUS c 
					 				 | expression_arith MINUS c
									 | c 
							
	'''
	if len(p) > 2:
		if p[2] is '+':
			crearCuadruploSuma()
		if p[2] is '-':
			crearCuadruploResta()

def p_c(p):

	'''
	
	c : c MULTIPLY te
		| c DIVIDE te
		| te 
	'''

	if len(p) > 2:
		if p[2] is '*':
			crearCuadruploMul()
		if p[2] is '/':
			crearCuadruploDiv()

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

	if p[1] is not '(':
		PilaOperandos.append(p[1]) 
	
def p_expression_logic(p):
	'''
	expression_logic : expression_logic OR g
					 | g				 
			
	'''
	if len(p) > 2:
		if p[2] is '|':
			crearCuadruploOR()
	
def p_g(p):

	'''
	g : g AND ge 
	  | ge

	'''
	if len(p) > 2:
		if p[2] is '&':
			crearCuadruploAND()
		
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
	
		if p[2] is not None:
			if p[2] == '==':
				crearCuadruploEQ()
			if p[2] is '>':
				crearCuadruploGT()
			if p[2] is '<':
				crearCuadruploLT()
			if p[2] == '>=':
				crearCuadruploGE()
			if p[2] == '<=':
				crearCuadruploLE()
			if p[2] == '<>':
				crearCuadruploNE()

def p_paso1IF(p):
	'''
	paso1IF : empty


	'''

	crearCuadruploGoToF()
	PiladeSaltos.append(cont - 1)

def p_paso2IF(p):
	'''
	paso2IF : empty

	'''

	crearCuadruploGoTo()
	direccion = PiladeSaltos.pop()
	Rellenar(direccion, cont)
	PiladeSaltos.append(cont - 1)

def p_paso3IF(p):
	'''
	paso3IF : empty
	'''

	global PiladeSaltos
	global cont

	direccion = PiladeSaltos.pop()

	Rellenar(direccion,cont)

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

def p_paso1DO(p):
	'''
	paso1DO : empty

	'''

	global PiladeSaltos

	PiladeSaltos.append(cont)

def p_paso2DO(p):
	'''

	paso2DO : empty

	'''

	crearCuadruploGoToV()

	direccion = PiladeSaltos.pop()

	Rellenar(len(Cuadruplos) - 1, direccion)

def p_paso1DoExit(p):
	'''
	paso1DoExit : empty

	'''

	global PiladeExits
	global PiladeSaltos
	PiladeExits.append(marca)
	PiladeSaltos.append(cont)

def p_paso2DoExit(p):
	'''
	paso2DoExit : empty

	'''

	crearCuadruploGoToDoExit()

def p_paso3DoExit(p):

	'''
	paso3DoExit : empty

	'''

	topPilaExits = PiladeExits.pop()

	while(topPilaExits != marca):
		Rellenar(topPilaExits,cont)
		topPilaExits = PiladeExits.pop()

def p_paso4DoExit(p):
	'''
	paso4DoExit : empty

	'''
	
	global PiladeExits
	PiladeExits.append(cont)

	crearCuadruploGoTo()

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
def ejecutor():

	global Cuadruplos
	global cont
	global tablaVariables

	i = 0
	print('\nEjecutor')
	while i < cont:
		cuad = Cuadruplos[i]
		operacion = cuad[0]

		if operacion == '+':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] + OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '=':
			OP1 = cuad[1]
			OP2 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value']
				tablaVariables[OP2]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')
		
		elif operacion == '*':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] * OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')
		
		elif operacion == '/':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] / OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')
		
		elif operacion == '-':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] - OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == 'goto':
			salto = cuad[1]
			i = salto - 1

		elif operacion == '<':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] < OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == 'gotoF':
			
			salto = cuad[2]
			condicion = cuad[1]
			OP1Info = tablaVariables.get(condicion)
			
			if OP1Info is not None:
				if OP1Info['value'] == False:
					i = salto - 1
			else:
				print('NO EXISTE LA VARIABLE')
	
		elif operacion == '>':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] > OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '<=':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] <= OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '>=':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] >= OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '<>':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] >= OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '==':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] == OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '&':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] and OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == '|':
			OP1 = cuad[1]
			OP2 = cuad[2]
			OP3 = cuad[3]

			OP1Info = tablaVariables.get(OP1)
			OP2Info = tablaVariables.get(OP2)

			if OP1Info is not None and OP2Info is not None:
				temp = OP1Info['value'] or OP2Info['value']
				tablaVariables[OP3]['value'] = temp
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == 'gotoV':
			
			salto = cuad[2]
			condicion = cuad[1]
			OP1Info = tablaVariables.get(condicion)
			
			if OP1Info is not None:
				if OP1Info['value'] == True:
					i = salto - 1
			else:
				print('NO EXISTE LA VARIABLE')

		elif operacion == 'read':
			
			lectura = ""

			while lectura == "":
				lectura = input("Input : ")
			OP1 = cuad[1]

			OP1Info = tablaVariables.get(OP1)

			if OP1Info is not None:
				tablaVariables[OP1]['value'] = int(lectura)
			else:
				print("NO EXISTE LA VARIABLE")
		
		elif operacion == 'outputS':

			stringImp = cuad[1]

			print("Output : ", stringImp)

		elif operacion == 'outputV':

			local = cuad[1]
			OP1Info = tablaVariables.get(local)
			print('Output' + ' ' + '"' + local + '"' + ': ' , OP1Info['value'])

		i = i + 1

print(code)
parser.parse(code)
ejecutor()
#Se necesita limpiar los valores cuando el ejecutor

#print(json.dumps(tablaVariables, indent = 2))

