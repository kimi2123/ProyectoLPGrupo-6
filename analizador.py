import tkinter as tk
from tkinter import scrolledtext 
from tkinter import ttk 
import ast 
from parser import analizar_codigo, imprimir_tabla_simbolos 
import io
import sys


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Código")
        self.root.geometry("1000x700") 
        self.root.config(bg="#F0F0F0") 

        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3) 
        self.root.grid_columnconfigure(1, weight=1) 

       
        self.left_panel = tk.Frame(self.root, bg="#FFFFFF", bd=0, relief="flat", padx=15, pady=15)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.left_panel.grid_rowconfigure(1, weight=1) 
        self.left_panel.grid_columnconfigure(0, weight=1)

        self.analyzer_label = tk.Label(self.left_panel, text="Analizador", font=("Helvetica Neue", 24, "bold"), bg="#FFFFFF", fg="#333333")
        self.analyzer_label.grid(row=0, column=0, sticky="nw", pady=(0, 15))

        self.code_editor = scrolledtext.ScrolledText(self.left_panel, wrap=tk.WORD, font=("Consolas", 11), bg="#F8F8F8", fg="#333333", insertbackground="black", bd=0, relief="flat", padx=10, pady=10)
        self.code_editor.grid(row=1, column=0, sticky="nsew")


        initial_code = """"""
        self.code_editor.insert(tk.END, initial_code)

    
        self.right_panel = tk.Frame(self.root, bg="#F0F0F0") 
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_panel.grid_rowconfigure(2, weight=1) 
        self.right_panel.grid_rowconfigure(3, weight=2) 
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Botón RUN
        self.run_button = tk.Button(self.right_panel, text="RUN", command=self.run_code,
                                    bg="#A2FF7F", fg="#333333", font=("Helvetica Neue", 14, "bold"),
                                    relief="flat", padx=20, pady=10, bd=0, highlightbackground="#A2FF7F", highlightthickness=0,
                                    activebackground="#8EDF6E") 
        self.run_button.grid(row=0, column=0, sticky="ne", pady=(0, 20)) 

        self.input_frame = tk.Frame(self.right_panel, bg="#FFFFFF", bd=0, relief="flat", padx=15, pady=15)
        self.input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_label = tk.Label(self.input_frame, text="Nombre del Tester", font=("Helvetica Neue", 16, "bold"), bg="#FFFFFF", fg="#333333")
        self.input_label.grid(row=0, column=0, sticky="nw", pady=(0, 10))

        self.input_text = scrolledtext.ScrolledText(self.input_frame, wrap=tk.WORD, height=5, font=("Consolas", 10), bg="#F8F8F8", fg="#333333", insertbackground="black", bd=0, relief="flat", padx=10, pady=10)
        self.input_text.grid(row=1, column=0, sticky="nsew")


        self.output_frame = tk.Frame(self.right_panel, bg="#FFFFFF", bd=0, relief="flat", padx=15, pady=15)
        self.output_frame.grid(row=2, column=0, sticky="nsew")
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_label = tk.Label(self.output_frame, text="Outputs de Logs", font=("Helvetica Neue", 16, "bold"), bg="#FFFFFF", fg="#333333")
        self.output_label.grid(row=0, column=0, sticky="nw", pady=(0, 10))

        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, height=10, font=("Consolas", 10), bg="#F8F8F8", fg="#333333", insertbackground="black", bd=0, relief="flat", padx=10, pady=10, state=tk.DISABLED)
        self.output_text.grid(row=1, column=0, sticky="nsew")

    def log_output(self, message):
        """Añade un mensaje al área de logs."""
        self.output_text.config(state=tk.NORMAL) 
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END) 
        self.output_text.config(state=tk.DISABLED) 

    def parse_and_evaluate(self, code_lines):
        """
        Simula la evaluación de las variables y expresiones básicas
        como se ve en el código de ejemplo.
        """
        variables = {}
        for line in code_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

  
            line = line.replace('true', 'True').replace('false', 'False')
            line = line.replace('||', 'or').replace('&&', 'and')
            
            try:
     
                if '=' in line and not line.startswith(('def', 'persona', 'numeros')):
                    parts = line.split('=', 1)
                    var_name = parts[0].strip()
                    expression_str = parts[1].split('#')[0].strip() 

                   
                    try:

                        exec_globals = {k: v for k, v in variables.items()}
                        evaluated_value = eval(expression_str, {"__builtins__": None}, exec_globals)
                        variables[var_name] = evaluated_value
                    except NameError as ne:
                        self.log_output(f"Error: Variable '{ne}' no definida al evaluar '{expression_str}'")
                    except SyntaxError as se:
                         self.log_output(f"Error de sintaxis al evaluar '{expression_str}': {se}")
                    except Exception as e:
                         self.log_output(f"Error inesperado al evaluar '{expression_str}': {e}")
                

                elif line.startswith("persona ="):
                    dict_str = line.split('=', 1)[1].strip().replace('=>', ':')
                    try:
                       
                        variables['persona'] = ast.literal_eval(dict_str)
                    except (ValueError, SyntaxError) as e:
                        self.log_output(f"Error al parsear 'persona': {e}")
                elif line.startswith("numeros ="):
                    list_str = line.split('=', 1)[1].strip()
                    try:
                        variables['numeros'] = ast.literal_eval(list_str)
                    except (ValueError, SyntaxError) as e:
                        self.log_output(f"Error al parsear 'numeros': {e}")

            except Exception as e:
                self.log_output(f"Error procesando línea '{line}': {e}")
        
        return variables


    def run_code(self):

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

        codigo = self.code_editor.get("1.0", tk.END)
        tester_name = self.input_text.get("1.0", tk.END).strip()

        if not tester_name:
            self.log_output("ERROR: Por favor, ingrese un 'Nombre del Tester' en el campo de input.")
            return
            
        if not codigo.strip():
            self.log_output("INFO: El editor de código está vacío. No hay nada que analizar.")
            return

        self.log_output(f"--- Iniciando Análisis (Tester: {tester_name}) ---")

        ast_result, errors_list = analizar_codigo(codigo, tester_name)

        # 4. Mostrar los resultados en el log de la GUI
        self.log_output("\n--- Resultados del Análisis ---")

        if errors_list:
            self.log_output("Se encontraron los siguientes errores:")
            for error in errors_list:
                self.log_output(f"-> {error}")
        else:
            self.log_output("¡Análisis completado exitosamente sin errores!")
            self.log_output(f"\nAST (Árbol de Sintaxis Abstracta) generado:")
            self.log_output(str(ast_result))

        self.log_output("\n--- Tabla de Símbolos Final ---")
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        imprimir_tabla_simbolos() 
        
        sys.stdout = old_stdout 
        tabla_str = captured_output.getvalue()
        
        self.log_output(tabla_str)

        self.log_output("\n--- Análisis Finalizado ---")



if __name__ == "__main__":
    root = tk.Tk() 
    app = CodeAnalyzerApp(root) 
    root.mainloop() 