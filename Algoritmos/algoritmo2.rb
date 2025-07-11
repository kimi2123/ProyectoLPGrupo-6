# =begin
# Algoritmo reducido para probar tokens, incluyendo variables, operadores, estructuras de control, 
# estructuras de datos y funciones.
# =end

# Variables
x = 10          
y = 5.5  
a = 5
b = 6
edad = 18       
nombre = "Juan" 
activo = true   

# Operadores Aritméticos
suma = x + y    
multiplicacion = x * 2  

# Operadores Lógicos
condicion_logica = (x > 5 || nombre == "Juan")

# Hash (estructura de datos)
persona = { "nombre" => "Carlos", "edad" => 30 }

# Array (estructura de datos)
numeros = [1, 2, 3, 4]

# Función para sumar
def sumar(a, b)
  return a + b
end

# Función para verificar edad
def es_mayor_de_edad(edad)
  return edad >= 18
end

# Uso de funciones
puts sumar(10, 5)  
puts es_mayor_de_edad(22) 

# Estructuras de control

# Condicional con operadores lógicos
if x == 10 && activo
  puts "x es 10 y activo es true"
else
  puts "Condición no cumplida"
end

# Bucle while
contador = 0
while contador < 3
  puts "Contador: #{contador}"
  contador += 1
end

# Bucle for sobre un Array
for num in numeros
  puts "Número en el Array: #{num}"
end

# Comparación con nil
if persona["activo"].nil?
  puts "El valor de activo es nil"
else
  puts "Activo: #{persona["activo"]}"
end

