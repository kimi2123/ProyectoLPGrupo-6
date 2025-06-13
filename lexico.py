import ply.lex as lex
import datetime
import os
import glob

ruta_carpeta="logs"
ruta_algoritmos="Algoritmos"
noReconocidos=[]


# Delimitadores y Palbras reservadas Luis Romero
reserved = {
    "true":"TRUE",
    "false":"FALSE",
    "if":"IF",
    "return":"RETURN",
    "else":"ELSE",
    "while":"WHILE",
    "in": "IN",
    "case": "CASE",
    "def": "DEF",
    "end": "END",
    "gets": "GETS",
    "each":"EACH",
    "elsif": "ELSEIF",
    "until":"UNTIL",
    "for": "FOR",
    "puts": "PUTS",
    "print": "PRINT",
    "do": "DO",

}


tokens = list(reserved.values()) + [
    'ANDAND', 'OROR', 'DIF', 'MASIGUAL', 'MENOSIGUAL', 'IGUAL', 'IGUALIGUAL', 'DIFIGUAL', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'ARROW', 'DOT',
    'COMMENTARIO', 'B_COMMENTARIO',
    'PARENTESIS_IZ', 'PARENTESIS_DER',
    'LLAVE_IZ', 'LLAVE_DER',
    'CORCHETE_IZ', 'CORCHETE_DER',
    'COMILLA_S', 'COMILLA_D',
    'INTERPOLACION',
    'Q_LLAVES', 'Q_PARENTESIS', 'Q_CORCHETES', 'Q_OTROS',
    'R_LLAVES', 'R_OTROS',
    'REGEX_SLASH',
    'ID',
    'INTEGER',
    'FLOAT',
    'STRING',
    'BOOLEAN',
    'COMA',
    'PIPE',
    'ARRAY',
    'VALOR_HASH',
    'HASH', 'SET',
    'NIL',
 ]

#Operadores y comentarios Ricardo Asanza
t_ANDAND = r'&&'
t_OROR = r'\|\|'
t_DIF = r'!'
t_MASIGUAL = r'\+='
t_MENOSIGUAL = r'-='
t_IGUAL = r'='
t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_IGUALIGUAL = r'=='
t_DIFIGUAL = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_COMMENTARIO = r'\#.*'
t_B_COMMENTARIO = r'=begin.*?=end'
t_PARENTESIS_IZ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZ = r'\['
t_CORCHETE_DER = r'\]'
t_COMILLA_S = r'\''
t_COMILLA_D = r'\"'
t_INTERPOLACION = r'\#\{'
t_Q_LLAVES = r'%[qQ]\{'
t_Q_PARENTESIS = r'%[qQ]\('
t_Q_CORCHETES = r'%[qQ]\['
t_Q_OTROS = r'%[qQ][^\w\s]'
t_R_LLAVES = r'%r\{'
t_R_OTROS = r'%r[^\w\s]'
t_REGEX_SLASH = r'/'
t_ARROW = r'=>'
t_DOT = r'\.'
t_COMA = r','
t_PIPE = r'\|'
t_ignore = ' \t'
#Variables y Tipos de datos Erick Danilo Armijos Romero

#Implementacion de los tipos de datos promitivos  y variables

def t_SET(t):
    r'Set\.new\(\s*\[.*\]\s*\)' 
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

def t_VALOR_HASH(t):
    r'[a-zA-z0-9_]*\["[a-zA-Z_][a-zA-Z0-9_]*"\]'
    t.type = 'ACCESO_HASH'
    return t

def t_ARRAY(t):
    r'\[([^\[\]]|\s)*\]'  
    return t

def t_HASH(t):
    r'\{[^}]*\}' 
    t.type = 'HASH'
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
    archivo = f"{ruta_algoritmos}/{algoritmo_file}"
    ahora = datetime.datetime.now()
    fecha_hora = ahora.strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"{log_prefix}-{fecha_hora}.txt"
    ruta_archivo = f"{ruta_carpeta}/{nombre_archivo}"

    with open(archivo, 'r') as f:
        contenido = f.read()
        lexer_instance.input(contenido)

    with open(ruta_archivo, "w") as archivo_log:
        while True:
            tok = lexer_instance.token()
            if not tok:
                break
            output = f"Token: tipo={tok.type}, valor='{tok.value}'"
            print(output)                        # ← Imprime en pantalla
            archivo_log.write(output + '\n')     # ← Guarda en archivo

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