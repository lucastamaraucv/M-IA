"""
Ventana con PESTANAS: junta la Pregunta 15 y la Pregunta 16 (y las que se
vayan agregando despues) en una sola aplicacion, cada una en su propia
pestana, sin perder la rotacion con el mouse ni el parpadeo de la leyenda.

Ejecutar:
    python preguntas.py

Requisitos:
    pip install numpy matplotlib
    (tkinter viene incluido con Python en Windows, no hace falta instalarlo)
"""

import os
import importlib.util
import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))


def cargar_modulo(nombre_archivo, nombre_modulo):
    """Carga 15.py / 16.py como modulo de Python a partir de su ruta.
    Se usa importlib (en vez de un 'import' normal) porque los nombres
    de archivo empiezan con un numero y no son identificadores validos
    de Python."""
    ruta = os.path.join(DIRECTORIO, nombre_archivo)
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def agregar_pestana(notebook, titulo, construir_figura):
    fig, anim, leyenda = construir_figura()

    pestana = ttk.Frame(notebook)
    notebook.add(pestana, text=titulo)

    canvas = FigureCanvasTkAgg(fig, master=pestana)
    canvas.draw()
    barra = NavigationToolbar2Tk(canvas, pestana)
    barra.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Hay que conservar referencias vivas a la figura/animacion/leyenda
    # y al timer de parpadeo: si Python los recolecta como basura al
    # salir de esta funcion, la animacion y el parpadeo se detienen.
    pestana._fig = fig
    pestana._anim = anim
    pestana._leyenda = leyenda
    pestana._canvas = canvas
    pestana._barra = barra
    return pestana


def main():
    mod15 = cargar_modulo('15.py', 'pregunta15')
    mod16 = cargar_modulo('16.py', 'pregunta16')

    root = tk.Tk()
    root.title('Examen - Preguntas 15 y 16 (visualizaciones interactivas)')
    root.geometry('1450x880')

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    agregar_pestana(notebook, 'Pregunta 15', mod15.construir_figura)
    agregar_pestana(notebook, 'Pregunta 16', mod16.construir_figura)

    root.mainloop()


if __name__ == '__main__':
    main()
