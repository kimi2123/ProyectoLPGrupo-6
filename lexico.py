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
}


tokens = list(reserved.values()) + [
    'PARENTESIS_IZ', 'PARENTESIS_DER',
    'LLAVE_IZ', 'LLAVE_DER',
    'CORCHETE_IZ', 'CORCHETE_DER',
    'COMILLA_S', 'COMILLA_D',
    'INTERPOLACION',
    'Q_LLAVES', 'Q_PARENTESIS', 'Q_CORCHETES', 'Q_OTROS',
    'R_LLAVES', 'R_OTROS',
    'REGEX_SLASH',
]


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
