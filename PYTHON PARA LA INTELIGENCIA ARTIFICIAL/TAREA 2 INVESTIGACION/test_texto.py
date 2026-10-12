import matplotlib
matplotlib.use('Agg')  # sin ventanas, solo para la prueba
import importlib, sys
sys.path.insert(0, '.')
# Redirigir el cwd para que encuentre el CSV
import os; os.chdir('C:\\Users\\Lucas Tamara\\Desktop\\M IA\\Python para la Inteligencia Artificial\\TAREA 2 INVESTIGACION')
exec(open('explicacion_codigo.py', encoding='utf-8').read())
