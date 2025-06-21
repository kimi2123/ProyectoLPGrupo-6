# Declaración de variables
nombre = "Ana"        # String
edad = 21             # Integer
altura = 1.65         # Float
es_estudiante = false # Boolean

# Operadores aritméticos
suma = edad + 5
multiplicacion = altura * 2
resta = edad - 3

# Operadores lógicos
mayor_edad = edad >= 18
estudiante_o_no = es_estudiante && mayor_edad

# Definición de una estructura de datos - Hash
persona = {
  "nombre" => nombre,
  "edad" => edad,
  "altura" => altura,
  "es_estudiante" => es_estudiante
}

# Imprimir valores
puts "El nombre es: #{persona["nombre"]}"
puts "La edad es: #{persona["edad"]}"
puts "Altura: #{persona["altura"]} metros"
puts "¿Es estudiante? #{persona["es_estudiante"]}"

# Condición if-else
if mayor_edad
  puts "#{nombre} es mayor de edad."
else
  puts "#{nombre} es menor de edad."
end

# Bucle while - Imprime el contador hasta 3
contador = 0
while contador < 3
  puts "Contador: #{contador}"
  contador += 1
end

# Definir una función para imprimir mensaje
def saludo(nombre)
  puts "Hola, #{nombre}!"
end

# Llamada a la función
saludo(nombre)

# Expresión aritmética y lógico-comparativa
if (edad + suma) > 30
  puts "La suma de la edad y la operación es mayor que 30."
else
  puts "La suma de la edad y la operación es menor o igual a 30."
end

