import ply.lex as lex

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
    "set": "SET",
}


tokens = list(reserved.values()) + [
    'ANDAND', 'OROR', 'DIF', 'MASIGUAL', 'MENOSIGUAL', 'IGUAL', 'IGUALIGUAL', 'DIFIGUAL', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD'
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
t_COMMENTARIO = r'#.*'
t_B_COMMENTARIO = r'=begin.*?=end'
t_PARENTESIS_IZ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZ = r'\['
t_CORCHETE_DER = r'\]'
t_COMILLA_S = r'\''
t_COMILLA_D = r'\"'
t_INTERPOLACION = r'#\{'
t_Q_LLAVES = r'%[qQ]\{'
t_Q_PARENTESIS = r'%[qQ]\('
t_Q_CORCHETES = r'%[qQ]\['
t_Q_OTROS = r'%[qQ][^\w\s]'
t_R_LLAVES = r'%r\{'
t_R_OTROS = r'%r[^\w\s]'
t_REGEX_SLASH = r'/'

#Variables y Tipos de datos Erick Danilo Armijos Romero

#Implementacion de los tipos de datos promitivos  y variables

def t_Id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_Float(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_String(t):
    r'"([^\\\n] | (\\.))*?"' 
    t.value = t.value[1:-1]
    return t

def t_Integer(t):
    r'\d+'
    t.value = int(t.value)
    return t



def t_Boolean(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_Nil(t):
    r'nil'
    t.value = None
    return t
    
#Implementacion para las estructuras de datos  
    
def t_Array(t):
    r'\[.*\]'
    return t

def t_Hash(t):
    r'\{.*\}'
    return t

def t_Set(t):
    r'set.new\([^\)]*\)'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineo += len(t.value)
    
def t_error(t):
    print(f"[Lexer] Linea {t.lineno}: caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)
    
def t_Comment(t):
    r'#.*'
    pass

def t_CommentarioMultiple(t):
    r'=begin.*?=end'
    pass
