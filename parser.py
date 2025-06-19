import ply.yacc as yacc
from lexico import lexer
import datetime
import os

# Ruta para guardar los archivos de log de errores sintácticos
ruta_carpeta = "logsErroresSintacticos"

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
    'declaracion : ARRAY ID PARENTESIS_IZ expresion PARENTESIS_DER'
    print(f"Array declarado: {p[2]} con valor {p[4]}")  # Imprime el nombre del array y su valor

# Producción para manejar el uso del array (ejemplo de acceso a elementos)
def p_acceso_array(p):
    'acceso : ID PARENTESIS_IZ expresion PARENTESIS_DER'
    print(f"Accediendo a {p[1]} en el índice {p[3]}")  # Accede al array usando un índice

# Producción para el ciclo FOR
def p_for_statement(p):
    'for : FOR ID IN expresion DO statement END'
    print(f"For loop detected: {p[1]} iterating over {p[3]}")
    p[0] = f"Iterating over {p[3]}"

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
