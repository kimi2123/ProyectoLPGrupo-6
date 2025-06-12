# Comentario de múltiples líneas
=begin
Este es un comentario
de varias líneas
=end

# Declaración de variables
nombre = "Juan"
edad = 25
altura = 1.75
es_estudiante = true
saludo = "Hola, soy #{nombre} y tengo #{edad} años."

# Estructuras de control
if edad >= 18
  puts "Mayor de edad"
else
  puts "Menor de edad"
end

# Uso de operador lógico
if edad >= 18 && es_estudiante
  puts "Es estudiante y mayor de edad"
end

contador = 0
while contador < 5
  puts "Contador: #{contador}"
  contador += 1
end

for i in 1..6
  puts "Iteración #{i}"
end

# Definición de función
def saludo(nombre)
  puts "Hola, #{nombre}!"
end

saludo("Carlos")

# Expresión aritmética con operadores
suma = 5 + 3
resta = 10 - 2
multiplicacion = 4 * 6
division = 10 / 2
modulo = 10 % 3

# Impresión de resultados
puts "Resultado de la suma: #{suma}"
puts "Resultado de la resta: #{resta}"
puts "Resultado de la multiplicación: #{multiplicacion}"
puts "Resultado de la división: #{division}"
puts "Resultado del módulo: #{modulo}"

# Declaración de estructuras de datos
arr = [1, 2, 3, 4, 5]
mi_hash = { "nombre" => "Juan", "edad" => 30, "ciudad" => "Madrid" }
mi_set = Set.new([1, 2, 3, 4, 5])

# Iterando sobre un hash
mi_hash.each do |clave, valor|
  puts "#{clave}: #{valor}"
end

# Definiendo una variable a partir de una operación
resultado = (5 * 2) + 3
puts "El resultado final es: #{resultado}"
