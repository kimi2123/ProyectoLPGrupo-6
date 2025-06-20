import ply.yacc as yacc
from lexico import lexer
import datetime
import os

# Ruta para guardar los archivos de log de errores sintácticos
ruta_carpeta = "logsErroresSintacticos"

def p_asignacion(t):
    'asignacion: ID IGUAL expresion'
    t[0] = f"{t[1]} = {t[3]}"
    
def p_impresion(t):
    '''impresion: PUTS " " expresion
    | PRINT " " expresion'''
    t[0] = f"Imprimir: {t[3]}"

def p_funcion(t):
    '''funcion: DEF ID PARENTESIS_IZ parametros PARENTESIS_DER 
    cuerpo END'''
    t[0] = f"Funcion: {t[2]} con los parametros {t[4]}"

def p_parametros(t):
    '''parametros: parametro 
    | parametro COMA parametros'''
    if len(t) == 2: 
        t[0] = [t[1]]
    else: 
        t[0] = [t[1]] + t[3]    

def p_parametro(t):
    'parametro: ID'

def p_set(t):
    '''set: SET PUNTO NEW PARENTESIS_IZ CORCHETE_IZ elementos CORCHETE_DER PARENTESIS_DER'''

def p_if(t):
    '''if: condiciones 
    cuerpo END'''
    t[0] = f"La condicion es: {t[2]} con su codigo: {t[3]}"

def p_ifelse(t):
    '''ifelse: condiciones 
    cuerpo ELSE cuerpo END'''
    t[0] = "La condicion es: {t[2]} con el bloque if: {t[3]} y else:{t[5]}" 

def p_expresion(t):
    '''expresion: ID
    | INTEGER
    | FLOAT
    | STRING
    | BOOLEAN'''

def p_cuerpo(t):
    '''cuerpo: linea
    | linea cuerpo'''

def p_linea(t):
    '''linea: impresion
    | asignacion'''
    
def p_elementos(t):
    '''elementos: expresion
                | expresion COMA elementos'''
    if len(t) == 2:
        t[0] = [t[1]]  
    else:
        t[0] = [t[1]] + t[3]

# Manejo de errores sintácticos
def p_error(t):
    # Si el error es un token, lo mostramos
    if t:
        print(f"Error de sintaxis en el token: {t.value}")
    else:
        print("Error sintáctico en la entrada.")
    
    # Pedir nombre del usuario para el log
    nombre_usuario = input("Por favor ingresa tu nombre: ")
    
    # Generar el nombre del archivo de log con fecha y hora
    ahora = datetime.datetime.now()
    fecha_hora = ahora.strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"sintactico-{nombre_usuario}-{fecha_hora}.txt"
    
    # Crear la ruta completa para el archivo de log
    ruta_archivo = os.path.join(os.path.dirname(__file__), ruta_carpeta, nombre_archivo)
    
    # Registrar el error en el archivo de log
    with open(ruta_archivo, "a") as archivo_log:
        archivo_log.write(f"Error: {t.value}\n")

# Luis Romero
# Definir la producción para manejar la declaración de un array
def p_declaracion_array(p):
    '''declaracion : ID IGUAL CORCHETE_IZ elementos CORCHETE_DER
    | ID IGUAL CORCHETE_IZ CORCHETE_DER '''
    print(f"Array declarado: {p[1]} con valor {p[4]}")  # Imprime el nombre del array y su valor


# Producción para manejar el uso del array (ejemplo de acceso a elementos)
def p_acceso_array(p):
    'acceso : ID PARENTESIS_IZ expresion PARENTESIS_DER'
    print(f"Accediendo a {p[1]} en el índice {p[3]}")  # Accede al array usando un índice

# Producción para el ciclo FOR
def p_for_statement(p):
    'for : FOR parametros IN expresion cuerpo END'
    print(f"For loop detected: {p[1]} iterating over {p[3]}")
    p[0] = f"Iterating over {p[3]}"

# Producción para el comando 'gets' (lectura desde el teclado)
def p_gets(p):
    'gets : GETS ID'
    variable = p[2]
    print(f"Ingrese el valor para {variable}: ", end="")
    valor = input()  # Llamamos a input() para que el usuario ingrese un valor
    print(f"Valor ingresado para {variable}: {valor}")
    p[0] = valor  # Asignamos el valor ingresado a la variable

# Continuar con las producciones adicionales para manejo de expresiones y sentencias






# Crear el parser
parser = yacc.yacc(module=None, debug=False, optimize=False)

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        try:
            s = input('Entrada > ')  # Lee la entrada
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)  # Procesa la entrada
        print(f"Resultado: {result}")
