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
    "or":"OR",
    "not":"NOT",
    "if":"IF",
    "return":"RETURN",
    "class":"CLASS",
    "module":"MODULE",
    "self":"SELF",
    "begin":"BEGIN",
    "else":"ELSE",
    "while":"WHILE",
    "and":"AND",
    "in": "IN",
    "case": "CASE",
    "def": "DEF",
    "end": "END",
    "printf": "PRINTF",
    "to_f": "TO_F",
    "concat": "CONCAT",
    "initialize" : "INITIALIZE",
    "gets": "GETS",
    "chomp": "CHOMP",
    "each":"EACH",
    "elsif": "ELSEIF",
    "until":"UNTIL",
    "for": "FOR",
    "sort": "SORT",
    "puts": "PUTS",
    "print": "PRINT",
    "do": "DO",
    "when" : "WHEN",
    "nil" : "NIL",
    "Array": "ARRAY",
    "Hash":  "HASH",
    "Set":   "SET",
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
    'ARRAY', 'ARRAY_CIERRE',
    'HASH_IZ', 'HASH_DER', 'HASH_ARROBA','SET', 'SET_CIERRE',
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


def t_ARRAY(t):
    r'\['  # Detecta el corchete de apertura
    t.type = 'PARENTESIS_IZ'  # Asignamos el tipo como corchete izquierdo
    return t

def t_ARRAY_CIERRE(t):
    r'\]'  # Detecta el corchete de cierre
    t.type = 'PARENTESIS_DER'  # Asignamos el tipo como corchete derecho
    return t

# Para los Hash, detectamos las llaves y el operador '=>'
def t_HASH_IZ(t):
    r'\{'  # Detecta la llave de apertura
    t.type = 'LLAVE_IZ'
    return t

def t_HASH_DER(t):
    r'\}'  # Detecta la llave de cierre
    t.type = 'LLAVE_DER'
    return t

def t_HASH_ARROBA(t):
    r'=>'
    t.type = 'ARROW'  # El operador de flecha
    return t

# Para Set, solo detectamos los paréntesis
def t_SET(t):
    r'set.new\('  # Detecta el inicio de un set
    t.type = 'PARENTESIS_IZ'
    return t

def t_SET_CIERRE(t):
    r'\)'  # Detecta el paréntesis de cierre
    t.type = 'PARENTESIS_DER'
    return t
  
# Manejo de espacios en blanco y saltos de linea

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

def log_function(lexer_instance, algoritmo_file, log_prefix):
    """
    Analiza un archivo Ruby y guarda el listado de tokens en /logs.
    
    Parameters
    ----------
    lexer_instance : el lexer ya construido con lex.lex()
    algoritmo_file : nombre de archivo Ruby (ej. 'algoritmo1.rb')
    log_prefix     : prefijo del archivo de log (ej. 'lexico')
    """

    # 1) Ruta ABSOLUTA al .rb dentro de Algoritmos/
    archivo_rb = os.path.join(os.path.dirname(__file__),
                              ruta_algoritmos, algoritmo_file)

    # 2) Crear carpeta logs/ si no existe
    os.makedirs(os.path.join(os.path.dirname(__file__), ruta_carpeta),
                exist_ok=True)

    # 3) Nombre de log con fecha-hora
    fecha_hora   = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_log   = f"{log_prefix}-{fecha_hora}.txt"
    ruta_log     = os.path.join(os.path.dirname(__file__),
                                ruta_carpeta, nombre_log)

    # 4) Cargar el código fuente en el lexer
    with open(archivo_rb, 'r', encoding='utf8') as f:
        lexer_instance.input(f.read())

    # 5) Abrir log y volcar tokens
    with open(ruta_log, "w", encoding='utf8') as archivo_log:
        while True:
            tok = lexer_instance.token()
            if not tok:
                break
            linea = f"Token: tipo={tok.type:<15} valor={tok.value!r}"
            print(linea)               # imprime en consola
            archivo_log.write(linea+'\n')

    print(f"\nResultado guardado en {ruta_log}")

lexer = lex.lex()

# ───────────────────────── Main de pruebas ─────────────────────────
if __name__ == "__main__":
    # Obtener todos los archivos .rb en orden alfabético
    algoritmos = sorted([os.path.basename(file_path) for file_path in glob.glob(os.path.join(os.path.dirname(__file__), ruta_algoritmos, "*.rb"))])

    # Procesar los archivos en orden
    for archivo in algoritmos:
        print(f"\n===== Analizando {archivo} =====")
        log_function(lexer, archivo, "lexico")