import ply.yacc as yacc
from lexico import tokens, lexer
import datetime
import os

# Directorio para logs de errores sintácticos
ruta_carpeta = "logsErroresSintacticos"

# Precedencia de operadores
precedence = (
    ('left', 'OROR'),
    ('left', 'ANDAND'),
    ('left', 'IGUALIGUAL', 'DIFIGUAL'),
    ('left', 'MAYORIGUAL', 'MENORIGUAL', 'MAYOR', 'MENOR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV', 'MOD'),
)

# Símbolo de inicio
start = 'cuerpo'

# ----------------------
# Reglas del parser
# ----------------------

def p_cuerpo(p):
    '''cuerpo : linea
              | linea cuerpo'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]


def p_linea(p):
    '''linea : impresion
             | asignacion
             | declaracion_array
             | acceso_array
             | declaracion_hash
             | for_statement
             | while_statement
             | set_statement
             | gets
             | funcion_definition
             | if_statement
             | ifelse_statement'''
    p[0] = p[1]


def p_impresion(p):
    '''impresion : PUTS expresion
                  | PRINT expresion'''
    p[0] = ('print', p[2])


def p_asignacion(p):
    'asignacion : ID IGUAL expresion'
    p[0] = ('assign', p[1], p[3])


def p_declaracion_array(p):
    'declaracion_array : ID IGUAL CORCHETE_IZ elementos CORCHETE_DER'
    p[0] = ('array_decl', p[1], p[4])


def p_acceso_array(p):
    'acceso_array : ID CORCHETE_IZ expresion CORCHETE_DER'
    p[0] = ('array_access', p[1], p[3])


def p_declaracion_hash(p):
    'declaracion_hash : ID IGUAL LLAVE_IZ pares_hash LLAVE_DER'
    p[0] = ('hash_decl', p[1], dict(p[4]))


def p_pares_hash(p):
    '''pares_hash : par_hash
                  | par_hash COMA pares_hash'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_par_hash(p):
    'par_hash : STRING ARROW expresion'
    p[0] = (p[1].strip('"'), p[3])


def p_for_statement(p):
    'for_statement : FOR ID IN expresion cuerpo END'
    p[0] = ('for', p[2], p[4], p[5])


def p_while_statement(p):
    'while_statement : WHILE condiciones cuerpo END'
    p[0] = ('while', p[2], p[3])


def p_set_statement(p):
    'set_statement : SET PUNTO NEW PARENTESIS_IZ CORCHETE_IZ elementos CORCHETE_DER PARENTESIS_DER'
    p[0] = ('set', p[5], p[7])


def p_gets(p):
    'gets : GETS ID'
    p[0] = ('input', p[2])


def p_funcion_definition(p):
    'funcion_definition : DEF ID PARENTESIS_IZ parametros PARENTESIS_DER cuerpo END'
    p[0] = ('def', p[2], p[4], p[6])


def p_if_statement(p):
    'if_statement : IF condiciones cuerpo END'
    p[0] = ('if', p[2], p[3])


def p_ifelse_statement(p):
    'ifelse_statement : IF condiciones cuerpo ELSE cuerpo END'
    p[0] = ('ifelse', p[2], p[3], p[5])


def p_parametros(p):
    '''parametros : parametro
                  | parametro COMA parametros'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]


def p_parametro(p):
    'parametro : ID'
    p[0] = p[1]


def p_elementos(p):
    '''elementos : expresion
                 | expresion COMA elementos'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]


def p_expresion_binop(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion'''
    ops = {'+': lambda x,y: x+y, '-': lambda x,y: x-y,
           '*': lambda x,y: x*y, '/': lambda x,y: x/y,
           '%': lambda x,y: x%y}
    p[0] = ops[p[2]](p[1], p[3])


def p_expresion_group(p):
    'expresion : PARENTESIS_IZ expresion PARENTESIS_DER'
    p[0] = p[2]


def p_expresion_int(p):
    'expresion : INTEGER'
    p[0] = p[1]


def p_expresion_float(p):
    'expresion : FLOAT'
    p[0] = p[1]


def p_expresion_id(p):
    'expresion : ID'
    p[0] = p[1]


def p_expresion_string(p):
    'expresion : STRING'
    p[0] = p[1]


def p_expresion_boolean(p):
    'expresion : BOOLEAN'
    p[0] = True if p[1].lower()=='true' else False


def p_condicion_rel(p):
    '''condicion : expresion IGUALIGUAL expresion
                  | expresion DIFIGUAL expresion
                  | expresion MAYOR expresion
                  | expresion MENOR expresion
                  | expresion MAYORIGUAL expresion
                  | expresion MENORIGUAL expresion'''
    p[0] = (p[2], p[1], p[3])


def p_condiciones(p):
    '''condiciones : condicion
                   | condiciones ANDAND condicion
                   | condiciones OROR condicion'''
    p[0] = p[1] if len(p)==2 else (p[2], p[1], p[3])


def p_error(p):
    if p:
        print(f"Error de sintaxis token='{p.value}' linea={p.lineno}")
    else:
        print("Error sintáctico EOF")

# Construcción del parser
parser = yacc.yacc(debug=False, optimize=False)

# Ejecución interactiva
if __name__=='__main__':
    while True:
        try:
            s = input('Entrada > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s, lexer=lexer)
        print(f"Resultado: {result}")
