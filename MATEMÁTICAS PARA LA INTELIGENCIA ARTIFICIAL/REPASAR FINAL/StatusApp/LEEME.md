# Indicador de estado (bandeja del sistema)

App en Python para Windows que muestra un icono en la bandeja del sistema
(junto al reloj) que cambia de color segun el estado de una tarea:

- 🟡 **Amarillo** = tarea en curso ("working")
- 🟢 **Verde** = tarea completada al 100% ("done")
- ⚪ Gris = sin tarea / inactivo

Corre en segundo plano y no requiere ventana visible.

## Como funciona

- `tray_app.py`: la app de bandeja. Lee cada 1.5s el archivo `status.txt`
  y pinta el icono en amarillo/verde/gris segun su contenido.
- `worker.py`: ejemplo de "tarea" que escribe `status.txt`. Al arrancar
  escribe `working`, hace su trabajo, y al terminar escribe `done`
  (o `error` si falla). Sustituye `do_task()` por tu proceso real.

Ambos procesos son independientes: `tray_app.py` solo mira el archivo
`status.txt`, así que puedes lanzar `worker.py` (o cualquier otro script
que escriba ese archivo) cuantas veces quieras y el indicador reaccionará.

## 1. Instalar dependencias

```
cd StatusApp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Probar en modo script (antes de compilar)

En una terminal:
```
python tray_app.py
```
Veras el icono gris en la bandeja del sistema.

En otra terminal:
```
python worker.py
```
El icono pasara a amarillo mientras corre `do_task()`, y a verde al
terminar.

## 3. Compilar a .exe con PyInstaller

Se generan dos ejecutables independientes: uno para el indicador
(sin consola, corre en segundo plano) y otro para el worker.

```
pyinstaller --noconfirm --onefile --windowed --name IndicadorEstado tray_app.py
pyinstaller --noconfirm --onefile --name TareaWorker worker.py
```

- `--windowed` (alias `--noconsole`) evita que aparezca una ventana de
  consola negra: el indicador queda realmente en segundo plano.
- Los `.exe` resultantes quedan en `dist\IndicadorEstado.exe` y
  `dist\TareaWorker.exe`.
- Copia ambos `.exe` a la MISMA carpeta para que compartan `status.txt`.

## 4. (Opcional) Arranque automatico con Windows

Crea un acceso directo a `IndicadorEstado.exe` y colocalo en:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```
para que el indicador arranque solo al iniciar sesion.

## Adaptarlo a tu propia tarea

Edita `do_task()` en `worker.py` y sustituye el bucle de ejemplo por el
proceso real que quieras vigilar (un script largo, una llamada a una
API, un pipeline, etc). Mientras ese codigo se ejecuta, el indicador
estara en amarillo; en cuanto `set_status("done")` se ejecute al final,
pasara a verde.
