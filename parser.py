import ply.yacc as yacc
from lexico import tokens, lexer
import datetime
import os
import re

# Directorio para logs de errores sintácticos
ruta_carpeta = "logsErroresSintacticos"
os.makedirs(ruta_carpeta, exist_ok=True)

ruta_logs_seman = "logsErroresSemanticos"
os.makedirs(ruta_logs_seman, exist_ok=True)

lista_errores = []

# Precedencia de operadores
precedence = (
    ('left', 'PUNTO'),
    ('left', 'OROR'),
    ('left', 'ANDAND'),
    ('left', 'IGUALIGUAL', 'DIFIGUAL'),
    ('left', 'MAYORIGUAL', 'MENORIGUAL', 'MAYOR', 'MENOR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV', 'MOD'),
)

#Actulizado por Luis R
tabla_simbolos = {
    "variables": {},
    "tipos": {},
    "str-funciones": ["len", "to_uppercase", "to_lowercase"],
}

contador_funcion = 0

# Símbolo de inicio
start = 'cuerpo'

# Reglas del parser
def get_expression_type(expr_node):
    if not isinstance(expr_node, tuple) or len(expr_node) == 0:
        return 'unknown'

    node_type = expr_node[0]
    if node_type in ('int', 'float', 'string', 'boolean', 'nil'):
        return node_type
    
    if node_type == 'id':
        var_name = expr_node[1]
        if var_name in tabla_simbolos['variables']:
            return get_expression_type(tabla_simbolos['variables'][var_name])
        return 'undefined_variable'

    if node_type == 'call_method':
        return expr_node[1]
    
    if node_type in ('==', '!=', '>', '<', '>=', '<=', 'ANDAND', 'OROR'):
        return 'boolean'

    return 'unknown'

def p_cuerpo(p):
    '''cuerpo : linea
              | linea cuerpo'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

#Hechas por Ricardo

def p_linea(p):
    '''linea : impresion
             | asignacion
             | expresion
             | declaracion_array
             | declaracion_hash
             | for_statement
             | while_statement
             | set_statement
             | gets
             | funcion_definition
             | if_statement
             | ifelse_statement
             | hashiterator
             | acceso_hash'''
    p[0] = p[1]


def p_impresion(p):
    '''impresion : PUTS expresion
                  | PRINT expresion'''
    p[0] = ('print', p[2])


def p_asignacion(p):
    'asignacion : ID IGUAL expresion'
    tabla_simbolos['variables'][p[1]] = p[3] 
    p[0] = ('assign', p[1], p[3])
   
#Actulizado por Luis R
def p_asignacion_plusigual(p):
    'asignacion : ID MASIGUAL expresion'
    if p[1] not in tabla_simbolos['variables']:
        log_error_seman(f"Error: la variable '{p[1]}' no ha sido definida para usar '+='.")

    expr_suma = ('+', ('id', p[1]), p[3])
    tabla_simbolos['variables'][p[1]] = expr_suma 
    p[0] = ('assign', p[1], expr_suma)

def p_asignacion_menosigual(p):
    'asignacion : ID MENOSIGUAL expresion'
    if p[1] not in tabla_simbolos['variables']:
        log_error_seman(f"Error: la variable '{p[1]}' no ha sido definida para usar '-='.")

    expr_resta = ('-', ('id', p[1]), p[3])
    tabla_simbolos['variables'][p[1]] = expr_resta 
    p[0] = ('assign', p[1], expr_resta)

#Actulizado por Luis R
def p_declaracion_array(p):
    '''declaracion_array : ID IGUAL CORCHETE_IZ CORCHETE_DER
    | ID IGUAL CORCHETE_IZ elementos CORCHETE_DER'''
    elementos_array = [] if len(p) == 5 else p[4]
    p[0] = ('array_decl', p[1], elementos_array)
    tabla_simbolos['variables'][p[1]] = ('array', elementos_array)
    
#Hechas por Ricardo
def p_acceso_hash(p):
    'acceso_hash : ID CORCHETE_IZ expresion CORCHETE_DER'
    p[0] = ('hash_access', p[1], p[3])

def p_expresion_accesonil(p):
    'expresion : acceso_hash PUNTO NIL INTERROGACION'
    p[0] = ('nil?', p[1])

#Actulizado por LUIS ROMERO
def p_declaracion_hash(p):
    '''declaracion_hash : ID IGUAL LLAVE_IZ LLAVE_DER
    | ID IGUAL LLAVE_IZ pares_hash LLAVE_DER'''
    if len(p) == 5:          # {} vacío
        valor_hash = {}
    else:
        pares = p[4]         # lista de tuplas (clave, valor)

        seen_keys = set()
        for k, v in pares:
            # Normalizamos la clave a representación de string sencilla
            # (puedes afinar según cómo representes STRING / INTEGER).
            clave_repr = repr(k)
            if clave_repr in seen_keys:
                log_error_seman(f"Error: clave duplicada en hash literal: {k}")
                p[0] = None
                return
            seen_keys.add(clave_repr)

        valor_hash = dict(pares)

    p[0] = ('hash_decl', p[1], valor_hash)
    tabla_simbolos['variables'][p[1]] = ('hash', valor_hash)


def p_pares_hash(p):
    '''pares_hash : par_hash
                  | par_hash COMA pares_hash'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_par_hash(p):
    'par_hash : STRING ARROW expresion'
    p[0] = (p[1], p[3])

#Hecha por Luis
def p_for_statement(p):
    'for_statement : FOR ID IN expresion cuerpo END'
    p[0] = ('for', p[2], p[4], p[5])

#Hechas por Erick
def p_while_statement(p):
    'while_statement : WHILE expresion cuerpo END'
    p[0] = ('while', p[2], p[3])


#Hecha por Ricardo
def p_set_statement(p):
    '''set_statement : ID IGUAL SET PUNTO NEW PARENTESIS_IZ CORCHETE_IZ CORCHETE_DER PARENTESIS_DER
    | ID IGUAL SET PUNTO NEW PARENTESIS_IZ CORCHETE_IZ elementos CORCHETE_DER PARENTESIS_DER'''
    if len(p) == 10:
        p[0] = ('set', [])
    else:
        p[0] = ('set', p[8])     

#Hecha por Luis
def p_gets(p):
    'gets : GETS ID'
    p[0] = ('input', p[2])

def p_parametros_opt(p):
    '''parametros_opt :
                      | parametros'''
    p[0] = [] if len(p) == 1 else p[1]

def p_funcion_start(p):
    'funcion_start : DEF ID PARENTESIS_IZ parametros_opt PARENTESIS_DER'
    global contador_funcion
    contador_funcion += 1      
    p[0] = (p[2], p[4])  
  
# Hecha por Ricardo
#   funcion_start devuelve (nombre_funcion, parametros)
#   cuerpo         devuelve la lista de sentencias del cuerpo
def p_funcion_definition(p):
    'funcion_definition : funcion_start cuerpo END'
    global contador_funcion

    nonmbre_funcion, parametros = p[1]  
    cuerpo_funcion           = p[2]      

    nombre_funcion = nonmbre_funcion

    tipos_parametros = {}
    for param in parametros:
        if param in tabla_simbolos['variables']:
            tipo = tabla_simbolos['variables'][param][0]
            tipos_parametros[param] = tipo
        else:
            tipos_parametros[param] = None

    tabla_simbolos[nombre_funcion] = {
        'parametros': parametros,
        'tipos_params': tipos_parametros,
    }
    contador_funcion -= 1

    p[0] = ('def', cuerpo_funcion, parametros, cuerpo_funcion)

#Hechas por Erick
#Regla semantica para validar que los parametros de una definicion sean los mismos cuando se llaman, hecha por Ricardo. 
def p_expresion_call(p):
    'expresion : ID PARENTESIS_IZ argumentos_opt PARENTESIS_DER'
    p[0] = ('Llamada', p[1], p[3])
    nombre_funcion = p[1]
    tipo_params = p[3] or []          

    if nombre_funcion not in tabla_simbolos:
        log_error_seman(f"Función '{nombre_funcion}' no declarada")
        p[0] = None
        return

    entry = tabla_simbolos[nombre_funcion]
    nombre_param = entry['parametros']                 
    tipos_esperado = entry['tipos_params']

    if len(tipo_params) != len(nombre_param):
        log_error_seman(
            f"La funcion {nombre_funcion} espera {len(nombre_param)} parametros y recibe {len(tipo_params)}"
        )
        return

    for i, (argumento, param_name) in enumerate(zip(tipo_params, nombre_param), start=1):
        tipo_esperado = tipos_esperado[param_name]
        tipo_real = get_expression_type(argumento)

        if tipo_real != tipo_esperado:
            log_error_seman(
                f"La función '{nombre_funcion}', parámetro #{i} ('{param_name}') debe ser '{tipo_esperado}' pero es '{tipo_real}'."
            )
            p[0] = None
            return


def p_argumentos_opt(p):
    '''argumentos_opt :  
                      | argumentos'''
    p[0] = [] if len(p)==1 else p[1]

def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos'''
    p[0] = [p[1]] if len(p)==2 else [p[1]]+p[3]

#Hechas por Ricardo:
def p_hashiterator(p): 
    'hashiterator : ID PUNTO EACH DO PIPE ID COMA ID PIPE cuerpo END'
    p[0] = ('hash_iterator', p[1],p[6],p[8])

def p_if_statement(p):
    'if_statement : IF expresion cuerpo END'
    p[0] = ('if', p[2], p[3])

def p_ifelse_statement(p):
    'ifelse_statement : IF expresion cuerpo ELSE cuerpo END'
    p[0] = ('if', p[2], p[3],'else', p[5])


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

#Hechas por Erick 
#Regla semantica para validar los tipos al hacer alguna op, hecha por Ricardo
def p_expresion_binop(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion'''
    
    op = p[2]
    izq = p[1]
    der = p[3]

    tipo_izq = get_expression_type(izq)
    tipo_der = get_expression_type(der)
    tipos_validos = ('int', 'float')

    if tipo_izq not in tipos_validos or tipo_der not in tipos_validos:
        log_error_seman(
            f"Error semántico, no puedes realizar la operación {op} con tipos de datos {tipo_izq} y {tipo_der}."
        )
        p[0] = ('error_binop', op, izq, der)
        return

    resultado_tipo = 'float' if 'float' in (tipo_izq, tipo_der) else 'int'

    p[0] = (resultado_tipo, (op, izq, der))


#Hecha por Luis
#Implementacion de regla semantica Erick Armijos
##Validación de que las operaciones de tipo booleano no se realicen con valores no booleanos
def p_expresion_cmp_logica(p):
    '''expresion : expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion IGUALIGUAL expresion
                 | expresion DIFIGUAL expresion
                 | expresion ANDAND expresion
                 | expresion OROR  expresion'''
    # Obtener los tipos de los operandos izquierdo y derecho
    tipo_izq = get_expression_type(p[1])
    tipo_der = get_expression_type(p[3])
    
    # Verificar que los tipos de los operandos sean compatibles
    if tipo_izq != tipo_der:
        log_error_seman(f"Error: comparación entre tipos incompatibles: {tipo_izq} y {tipo_der}.")
        p[0] = None  # No realizar la comparación si los tipos no son compatibles
        return
    
    # Si los tipos son compatibles, continuar con la comparación
    p[0] = (p[2], p[1], p[3])

def p_expresion_group(p):
    'expresion : PARENTESIS_IZ expresion PARENTESIS_DER'
    p[0] = p[2]

def p_expresion_int(p):
    'expresion : INTEGER'
    p[0] = ('int', p[1])


def p_expresion_float(p):
    'expresion : FLOAT'
    p[0] = ('float', p[1])



#Actulizado por Luis R
def p_expresion_id(p):
    'expresion : ID'

    if p[1] not in tabla_simbolos['variables'] and p[1] not in tabla_simbolos: 
        log_error_seman(f"La variable o función '{p[1]}' no ha sido definida.")
        p[0] = ('error', f"variable no definida: {p[1]}")
    else:
        p[0] = ('id', p[1]) 

def p_expresion_string(p):
    'expresion : STRING'
    p[0] = ("string", p[1])

def p_expresion_boolean(p):
    '''expresion : BOOLEAN
                 | TRUE
                 | FALSE '''
    valor_booleano = str(p[1]).lower() == 'true'
    p[0] = ('boolean', valor_booleano)

# Regla Semántica de validacion de funciones sobre Strings Luis Romero
def p_expresion_metodo_string(p):
    'expresion : expresion PUNTO ID PARENTESIS_IZ PARENTESIS_DER'
    nodo_objeto = p[1]
    nombre_metodo = p[3]

    if nombre_metodo not in tabla_simbolos['str-funciones']:
        log_error_seman(f"Error semántico: '{nombre_metodo}' no es una función de string reconocida. Las funciones válidas son: {tabla_simbolos['str-funciones']}.")
        p[0] = ('error_metodo_desconocido',) 
        return

    tipo_objeto = get_expression_type(nodo_objeto)
    
    if tipo_objeto != 'string':
        log_error_seman(f"Error semántico: La función '{nombre_metodo}()' solo se puede llamar sobre un tipo 'string', pero se intentó usar en un tipo '{tipo_objeto}'.")
        p[0] = ('error_tipo_incorrecto_metodo',) 
        return

    tipo_retorno = 'unknown'
    if nombre_metodo == 'len':
        tipo_retorno = 'int'
    elif nombre_metodo in ('to_uppercase', 'to_lowercase'):
        tipo_retorno = 'string'
        
    p[0] = ('call_method', tipo_retorno, nodo_objeto, nombre_metodo)


def p_expresion_nil(p):
    'expresion : NIL'
    p[0] = ('nil',)
    
def p_linea_return(p):
    'linea : RETURN expresion'
    if contador_funcion == 0:
        log_error_seman("Error: 'return' fuera de cualquier funcion")
        p[0] = None
        return
    p[0] = ('return', p[2])

def imprimir_tabla_simbolos():
    # Imprimir los contenidos de la tabla de símbolos
    print("Contenido de la tabla de símbolos:")
    for nombre, datos in tabla_simbolos.items():
        print(f"{nombre}: {datos}")

def p_error(p):
    global tester_name
    # timestamp al principio de la ejecución, solo una vez
    if not hasattr(p_error, 'log_file'):  # Si no tiene el archivo de log
        ts = datetime.datetime.now().strftime("%d%m%Y-%Hh%M%S")
        nombre = tester_name or "anonimo"
        nombre_f = f"sintactico-{nombre}-{ts}.txt"
        p_error.log_file = os.path.join(ruta_carpeta, nombre_f)  # Asigna el archivo de log

    if p:
        msg = f"Error de sintaxis token='{p.value}' linea={p.lineno}\n"
    else:
        msg = "Error sintáctico: fin de archivo inesperado (EOF)\n"

    # Escribe los errores en el mismo archivo
    with open(p_error.log_file, "a", encoding="utf-8") as f:
        f.write(msg)
    lista_errores.append(msg.strip())
    print(msg.strip())

# Construcción del parser
parser = yacc.yacc(debug=False, optimize=False)

def log_error_seman(msg):
    if not hasattr(log_error_seman, 'log_file'):
        ts = datetime.datetime.now().strftime("%d%m%Y-%Hh%M%S")
        nombre = tester_name or "anonimo"
        nombre_f = f"semantico-{nombre}-{ts}.txt"
        
        # Obtén la ruta absoluta del directorio actual del proyecto
        proyecto_dir = os.getcwd()  # Esto obtiene el directorio actual
        log_path = os.path.join(proyecto_dir, ruta_logs_seman, nombre_f)  # Ruta correcta
        log_error_seman.log_file = log_path
    
    with open(log_error_seman.log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print("[Error semántico]", msg)
    error_completo = f"[Error semántico] {msg}"
    lista_errores.append(error_completo) 

tester_name = "default_user"

def analizar_codigo(codigo_fuente, nombre_tester):

    global tester_name, lista_errores, tabla_simbolos, contador_funcion
    
    tester_name = nombre_tester
    lista_errores.clear()
    

    tabla_simbolos.clear()
    tabla_simbolos.update({
        "variables": {},
        "tipos": {},
        "str-funciones": ["len", "to_uppercase", "to_lowercase"],
    })
    contador_funcion = 0

    if hasattr(p_error, 'log_file'):
        delattr(p_error, 'log_file')
    if hasattr(log_error_seman, 'log_file'):
        delattr(log_error_seman, 'log_file')
        
    lexer.lineno = 1

    if not codigo_fuente.strip():
        return None, ["No se ingresó código para analizar."]

    try:
        resultado = parser.parse(codigo_fuente, lexer=lexer)
    except Exception as e:
        lista_errores.append(f"Error crítico en el parser: {e}")
        resultado = None

    return resultado, lista_errores

if __name__=='__main__':
    # Pedimos el nombre del tester una sola vez
    tester_name = input("¿Quién hace el test? ").strip()
    if not tester_name:
        print("Debes ingresar un nombre. Terminando.")
        exit()

    # Bucle para realizar múltiples tests
    while True:
        try:
            # Leemos la entrada a parsear
            s = input('Entrada > ')
        except EOFError:
            break
        if not s:
            continue

        if not s.strip():
            continue

        result, errores = analizar_codigo(s, tester_name)

        # 2) FILTRO: rutas de Windows o comandos (& ...)
        if s.startswith('& ') or re.match(r'^[A-Za-z]:(\\|/)', s):
            # simplemente las descartamos
            continue

        if errores:
            print("Se encontraron los siguientes errores:")
            for err in errores:
                print(f"- {err}")
        else:
            print("Análisis completado sin errores.")
            print(f"Resultado AST: {result}")

        # Ejecutamos el parser
        result = parser.parse(s, lexer=lexer)
        print(f"Resultado: {result}")

        
        imprimir_tabla_simbolos()