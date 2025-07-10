import ply.lex as lex
import datetime
import os
import glob
import datetime

ruta_carpeta = "logs"
ruta_algoritmos = "Algoritmos"
noReconocidos = []

# Delimitadores y Palabras reservadas Luis Romero
reserved = {
    "true": "TRUE",
    "false": "FALSE",
    "if": "IF",
    "return": "RETURN",
    "else": "ELSE",
    "while": "WHILE",
    "in": "IN",
    "def": "DEF",
    "end": "END",
    "gets": "GETS",
    "each": "EACH",
    "for": "FOR",  
    "puts": "PUTS",
    "print": "PRINT",
    "do": "DO",
    "nil": "NIL", 
}

# Cambiar: Eliminar 'NIL' y 'DOT' de tokens porque ya están definidos más abajo
tokens = list(reserved.values()) + [
    'SET', 'NEW', 'ANDAND', 'OROR', 'MASIGUAL', 'MENOSIGUAL', 'MAYORIGUAL', 'MENORIGUAL',
    'IGUAL', 'IGUALIGUAL', 'DIFIGUAL', 'MAYOR', 'MENOR', 
    'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'ARROW', 
    'COMMENTARIO', 'B_COMMENTARIO', 'PARENTESIS_IZ', 'PARENTESIS_DER', 'LLAVE_IZ', 
    'LLAVE_DER', 'CORCHETE_IZ', 'CORCHETE_DER',
    'ID', 'INTEGER', 'FLOAT', 'STRING', 'BOOLEAN', 'COMA', 'PIPE', 'INTERROGACION', 'PUNTO'
]

# Operadores y comentarios
t_ANDAND = r'&&'
t_OROR = r'\|\|'
t_MASIGUAL = r'\+='
t_MENOSIGUAL = r'-='
t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_ARROW = r'=>'
t_IGUALIGUAL = r'=='
t_DIFIGUAL = r'!='
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_IGUAL = r'='
t_MAYOR = r'>'
t_MENOR = r'<'
t_COMMENTARIO = r'\#.*'
t_B_COMMENTARIO = r'=begin.*?=end'
t_PARENTESIS_IZ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','
t_PUNTO = r'\.'
t_PIPE = r'\|'
t_INTERROGACION = r'\?'
t_ignore = ' \t\n'

# Variables y Tipos de datos Erick Danilo Armijos Romero

def t_NEW(t):
    r'\bnew\b'  # Detecta la palabra 'new'
    t.type = 'NEW'
    return t

def t_GETS(t):
    r'\bgets\b' 
    t.type = 'GETS' 
    return t

def t_SET(t):
    r'\bSet\b' 
    t.type = 'SET'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"([^\\\n] | (\\.))*?"'
    t.value = t.value[1:-1]
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_NIL(t):
    r'nil'
    t.value = None
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print(f"[Lexer] Linea {t.lineno}: caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def t_Comment(t):
    r'\#.*'
    pass

def t_CommentarioMultiple(t):
    r'=begin[\s\S]*?=end'
    pass

def log_function(lexer_instance, algoritmo_file, log_prefix):
    nombre_usuario = input("Por favor ingresa tu nombre: ")

    # Construcción correcta de la ruta al archivo
    archivo = os.path.join(os.path.dirname(__file__), ruta_algoritmos, algoritmo_file)

    # Asegurarse de que el archivo se está abriendo correctamente
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()
            lexer_instance.input(contenido)  
    except FileNotFoundError:
        print(f"[Error] No se encontró el archivo: {archivo}")
        return

    # Crear archivo de log
    ahora = datetime.datetime.now()
    fecha_hora = ahora.strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"{log_prefix}-{nombre_usuario}-{fecha_hora}.txt"
    ruta_archivo = os.path.join(os.path.dirname(__file__), ruta_carpeta, nombre_archivo)

    with open(ruta_archivo, "a") as archivo_log:
        while True:
            tok = lexer_instance.token() 
            if not tok: 
                break
            output = f"Token: tipo={tok.type}, valor='{tok.value}'"
            print(output)  # Imprime en pantalla
            archivo_log.write(output + '\n')  # Guarda en archivo

    print(f"\nResultado guardado en {ruta_archivo}")

lexer = lex.lex()    

# ───────────────────────── Main de pruebas ─────────────────────────
if __name__ == "__main__":
    # Obtener todos los archivos .rb 
    algoritmos = sorted([os.path.basename(file_path) for file_path in glob.glob(os.path.join(os.path.dirname(__file__), ruta_algoritmos, "*.rb"))])

    # Procesar los archivos en orden
    for archivo in algoritmos:
        print(f"\n===== Analizando {archivo} =====")
        log_function(lexer, archivo, "lexico")
