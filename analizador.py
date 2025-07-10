import tkinter as tk
from tkinter import scrolledtext, ttk
import io
import sys

# Importa tu parser y funciones de análisis
from parser import analizar_codigo, imprimir_tabla_simbolos


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Código")
        self.root.geometry("1000x700")
        self.root.config(bg="#F0F0F0")

        # Layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        # Left panel
        self.left_panel = tk.Frame(self.root, bg="#FFFFFF", padx=15, pady=15)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.left_panel.grid_rowconfigure(1, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        tk.Label(self.left_panel, text="Analizador", font=("Helvetica Neue", 24, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="nw", pady=(0, 15))
        self.code_editor = scrolledtext.ScrolledText(self.left_panel, wrap=tk.WORD, font=("Consolas", 11), bg="#F8F8F8", padx=10, pady=10)
        self.code_editor.grid(row=1, column=0, sticky="nsew")

        # Right panel
        self.right_panel = tk.Frame(self.root, bg="#F0F0F0")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_panel.grid_rowconfigure(2, weight=1)
        self.right_panel.grid_rowconfigure(3, weight=2)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.run_button = tk.Button(self.right_panel, text="RUN", command=self.run_code,
                                    bg="#A2FF7F", fg="#333333", font=("Helvetica Neue", 14, "bold"),
                                    relief="flat", padx=20, pady=10)
        self.run_button.grid(row=0, column=0, sticky="ne", pady=(0, 20))

        # Tester name input
        self.input_frame = tk.Frame(self.right_panel, bg="#FFFFFF", padx=15, pady=15)
        self.input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        tk.Label(self.input_frame, text="Nombre del Tester", font=("Helvetica Neue", 16, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="nw", pady=(0,10))
        self.input_text = scrolledtext.ScrolledText(self.input_frame, wrap=tk.WORD, height=5, font=("Consolas", 10), bg="#F8F8F8", padx=10, pady=10)
        self.input_text.grid(row=1, column=0, sticky="nsew")

        # Logs output
        self.output_frame = tk.Frame(self.right_panel, bg="#FFFFFF", padx=15, pady=15)
        self.output_frame.grid(row=2, column=0, sticky="nsew")
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        tk.Label(self.output_frame, text="Outputs de Logs", font=("Helvetica Neue", 16, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="nw", pady=(0,10))
        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, height=10, font=("Consolas", 10), bg="#F8F8F8", padx=10, pady=10, state=tk.DISABLED)
        self.output_text.grid(row=1, column=0, sticky="nsew")

    def log_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def run_code(self):
        # Clear previous logs
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

        codigo = self.code_editor.get("1.0", tk.END)
        tester_name = self.input_text.get("1.0", tk.END).strip()
        if not tester_name:
            self.log_output("ERROR: Por favor, ingrese un 'Nombre del Tester'.")
            return
        if not codigo.strip():
            self.log_output("INFO: El editor de código está vacío.")
            return

        self.log_output(f"--- Iniciando Análisis (Tester: {tester_name}) ---")

        # Capture both stdout and stderr from the lexer/parser
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        try:
            ast_result, errors_list = analizar_codigo(codigo, tester_name)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        # Extract lexical messages from stdout/stderr and filter lexer-only
        all_messages = stdout_capture.getvalue().splitlines() + stderr_capture.getvalue().splitlines()
        lex_messages = [m for m in all_messages if m.startswith("[Lexer]")]

        self.log_output("- Resultados del Análisis ---")

        # First, log lexical errors 
        if lex_messages:
            self.log_output("Errores Léxicos detectados:")
            for msg in lex_messages:
                self.log_output(f"-> {msg}")

        # Then, log semantic/parser errors
        if errors_list:
            self.log_output("Se encontraron los siguientes errores semánticos:")
            for error in errors_list:
                self.log_output(f"-> {error}")
        elif not lex_messages:
            self.log_output("¡Análisis completado exitosamente sin errores!")
            self.log_output("\nAST generado:")
            self.log_output(str(ast_result))

        # Finally, print symbol table
        self.log_output("\n--- Tabla de Símbolos Final ---")
        old_stdout2 = sys.stdout
        stdout_capture2 = io.StringIO()
        sys.stdout = stdout_capture2
        imprimir_tabla_simbolos()
        sys.stdout = old_stdout2
        for line in stdout_capture2.getvalue().splitlines():
            self.log_output(line)

        self.log_output("\n--- Análisis Finalizado ---")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()
