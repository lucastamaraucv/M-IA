#!/usr/bin/env python3
"""
Python Code Visualizer - Interfaz gráfica para ejecutar código paso a paso
Similar a PythonTutor pero ejecutado localmente en tu PC
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
from io import StringIO
import linecache
import inspect

class PythonVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Visualizer")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Estado de ejecución
        self.execution_state = {
            'lines': [],
            'current_line_index': -1,
            'variables': {},
            'output': '',
            'finished': False,
            'globals': {},
            'locals': {}
        }
        
        self.setup_ui()
        self.apply_styles()
        
    def apply_styles(self):
        """Aplica estilos a la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        bg_color = "#f0f0f0"
        fg_color = "#333333"
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', font=('Arial', 9))
        
    def setup_ui(self):
        """Configura la interfaz gráfica"""
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== COLUMNA IZQUIERDA: Editor de código =====
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        title_label = ttk.Label(left_frame, text="📝 Código Python", font=("Arial", 11, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Editor de código
        self.code_editor = scrolledtext.ScrolledText(
            left_frame,
            height=20,
            width=50,
            font=("Courier New", 10),
            bg="white",
            fg="#333",
            insertbackground="#0066cc"
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Ejemplo inicial
        example_code = """# Ejemplo: Cálculo de promedio
numeros = [8, 9, 7, 10]
suma = 0

for num in numeros:
    suma = suma + num

promedio = suma / len(numeros)
print(f"Promedio: {promedio}")"""
        self.code_editor.insert("1.0", example_code)
        
        # Botones de control
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.reset_btn = ttk.Button(
            button_frame,
            text="↻ Reiniciar",
            command=self.reset_execution
        )
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.step_btn = ttk.Button(
            button_frame,
            text="► Paso siguiente",
            command=self.step_forward
        )
        self.step_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.execute_all_btn = ttk.Button(
            button_frame,
            text="▶▶ Ejecutar todo",
            command=self.execute_all
        )
        self.execute_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.example_btn = ttk.Button(
            button_frame,
            text="📚 Cargar Ejemplo",
            command=self.load_example
        )
        self.example_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_label = ttk.Label(
            left_frame,
            text="Esperando código...",
            font=("Arial", 9),
            foreground="#666"
        )
        self.status_label.pack(anchor=tk.W)
        
        # ===== COLUMNA DERECHA: Visualización =====
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        title_label2 = ttk.Label(right_frame, text="🔍 Ejecución en tiempo real", font=("Arial", 11, "bold"))
        title_label2.pack(anchor=tk.W, pady=(0, 10))
        
        # Línea actual
        line_label = ttk.Label(right_frame, text="Línea actual:", font=("Arial", 9, "bold"))
        line_label.pack(anchor=tk.W)
        
        self.line_display = tk.Text(
            right_frame,
            height=2,
            bg="#e6f1fb",
            fg="#042c53",
            font=("Courier New", 10),
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.line_display.pack(fill=tk.X, pady=(0, 10))
        self.line_display.insert("1.0", "Presiona 'Paso siguiente' para comenzar")
        
        # Variables
        var_label = ttk.Label(right_frame, text="Variables:", font=("Arial", 9, "bold"))
        var_label.pack(anchor=tk.W)
        
        self.variables_display = scrolledtext.ScrolledText(
            right_frame,
            height=8,
            bg="white",
            fg="#333",
            font=("Courier New", 9),
            relief=tk.FLAT
        )
        self.variables_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.variables_display.insert("1.0", "Sin variables aún")
        self.variables_display.config(state=tk.DISABLED)
        
        # Salida
        output_label = ttk.Label(right_frame, text="Salida (print):", font=("Arial", 9, "bold"))
        output_label.pack(anchor=tk.W)
        
        self.output_display = scrolledtext.ScrolledText(
            right_frame,
            height=6,
            bg="white",
            fg="#333",
            font=("Courier New", 9),
            relief=tk.FLAT
        )
        self.output_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.output_display.insert("1.0", "Sin salida")
        self.output_display.config(state=tk.DISABLED)
        
        # Status detail
        self.detail_label = ttk.Label(
            right_frame,
            text="",
            font=("Arial", 8),
            foreground="#666"
        )
        self.detail_label.pack(anchor=tk.W)
        
    def load_example(self):
        """Carga un ejemplo de código"""
        self.code_editor.delete("1.0", tk.END)
        example = """# Ejemplo: Cálculo de promedio
numeros = [8, 9, 7, 10]
suma = 0

for num in numeros:
    suma = suma + num

promedio = suma / len(numeros)
print(f"Promedio: {promedio}")"""
        self.code_editor.insert("1.0", example)
        self.reset_execution()
        
    def reset_execution(self):
        """Reinicia la ejecución del código"""
        code = self.code_editor.get("1.0", tk.END)
        lines = [line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        self.execution_state = {
            'lines': lines,
            'current_line_index': -1,
            'variables': {},
            'output': '',
            'finished': False,
            'globals': {},
            'locals': {}
        }
        
        self.update_display()
        self.status_label.config(text=f"✓ {len(lines)} líneas cargadas. Listo para ejecutar.")
        
    def step_forward(self):
        """Ejecuta la siguiente línea"""
        if self.execution_state['current_line_index'] >= len(self.execution_state['lines']) - 1:
            self.execution_state['finished'] = True
            self.status_label.config(text="✓ Ejecución completada")
            self.step_btn.config(state=tk.DISABLED)
            self.update_display()
            return
        
        self.execution_state['current_line_index'] += 1
        current_line = self.execution_state['lines'][self.execution_state['current_line_index']]
        
        try:
            self.execute_line(current_line)
        except Exception as e:
            self.status_label.config(text=f"⚠ Error: {str(e)}")
            self.execution_state['output'] += f"\n❌ Error: {str(e)}"
        
        self.update_display()
        
    def execute_line(self, line):
        """Ejecuta una línea de código y actualiza el estado"""
        line = line.strip()
        
        # Combinar globals y locals
        exec_globals = {**self.execution_state['globals']}
        exec_locals = {**self.execution_state['locals']}
        
        # Variables built-in necesarias
        exec_globals.update({
            'print': self.custom_print,
            'len': len,
            'range': range,
            'sum': sum,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
        })
        
        try:
            # Intentar ejecutar la línea
            exec(line, exec_globals, exec_locals)
            
            # Actualizar el estado
            self.execution_state['globals'] = exec_globals
            self.execution_state['locals'] = exec_locals
            
        except Exception as e:
            raise e
    
    def custom_print(self, *args, **kwargs):
        """Función print personalizada que captura la salida"""
        output = ' '.join(str(arg) for arg in args)
        self.execution_state['output'] += output + '\n'
        
    def execute_all(self):
        """Ejecuta todo el código de una vez"""
        self.reset_execution()
        while self.execution_state['current_line_index'] < len(self.execution_state['lines']) - 1:
            self.step_forward()
        
    def update_display(self):
        """Actualiza la visualización de estado"""
        # Actualizar línea actual
        self.line_display.config(state=tk.NORMAL)
        self.line_display.delete("1.0", tk.END)
        
        if (self.execution_state['current_line_index'] >= 0 and 
            self.execution_state['current_line_index'] < len(self.execution_state['lines'])):
            line = self.execution_state['lines'][self.execution_state['current_line_index']]
            self.line_display.insert("1.0", f"► {line}")
            self.line_display.config(bg="#e6f1fb", fg="#042c53")
        else:
            self.line_display.insert("1.0", "Presiona 'Paso siguiente' para comenzar")
            self.line_display.config(bg="#f5f5f5", fg="#999")
        
        self.line_display.config(state=tk.DISABLED)
        
        # Actualizar variables
        self.variables_display.config(state=tk.NORMAL)
        self.variables_display.delete("1.0", tk.END)
        
        if self.execution_state['locals']:
            for key, value in self.execution_state['locals'].items():
                if not key.startswith('_'):
                    value_str = repr(value)
                    if len(value_str) > 50:
                        value_str = value_str[:47] + "..."
                    self.variables_display.insert(tk.END, f"{key} = {value_str}\n")
        else:
            self.variables_display.insert("1.0", "Sin variables aún")
        
        self.variables_display.config(state=tk.DISABLED)
        
        # Actualizar salida
        self.output_display.config(state=tk.NORMAL)
        self.output_display.delete("1.0", tk.END)
        
        output = self.execution_state['output'].strip()
        if output:
            self.output_display.insert("1.0", output)
        else:
            self.output_display.insert("1.0", "Sin salida")
        
        self.output_display.config(state=tk.DISABLED)
        
        # Actualizar label de detalle
        idx = self.execution_state['current_line_index'] + 1
        total = len(self.execution_state['lines'])
        self.detail_label.config(text=f"Línea {idx}/{total}")
        
        # Actualizar estado del botón
        if self.execution_state['finished']:
            self.step_btn.config(state=tk.DISABLED)
        else:
            self.step_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = PythonVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
