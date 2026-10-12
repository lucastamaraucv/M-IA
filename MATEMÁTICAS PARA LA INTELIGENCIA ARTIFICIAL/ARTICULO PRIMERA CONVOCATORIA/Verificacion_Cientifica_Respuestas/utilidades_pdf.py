"""
Utilidades compartidas por los 16 scripts pregunta_XX.py de esta carpeta.

METODO CIENTIFICO APLICADO A PREGUNTAS DE LECTURA (1-13):
  No se "opina" sobre cual alternativa es correcta. Se abre el PDF ORIGINAL
  del articulo con PyMuPDF (fitz), se extrae su texto real y se busca -de
  forma automatica y reproducible, con str.find()- la cita textual exacta
  que respalda la respuesta marcada en respuestas_examen_verificadas.txt.
  Si la cita NO aparece en el PDF, el script lo reporta como FALLO (no se
  inventa ni se fuerza el resultado). Ademas, cuando es posible, se busca
  tambien una frase que CONTRADIGA a cada alternativa incorrecta.

METODO CIENTIFICO APLICADO A PREGUNTAS DE OPTIMIZACION (14-16):
  Ademas de la verificacion textual anterior, se ejecuta una comprobacion
  NUMERICA independiente (numpy): se construyen contraejemplos concretos,
  se calculan autovalores del Hessiano y/o se corre una simulacion de
  Monte Carlo del descenso por gradiente, y se compara el resultado
  medido contra lo que afirma cada alternativa.
"""

import os
import re
import sys
import fitz  # PyMuPDF

# Este archivo vive en .../ARTICULO PRIMERA CONVOCATORIA/Verificacion_Cientifica_Respuestas/
# Los 4 PDF originales de los articulos estan un nivel arriba.
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CARPETA_PROYECTO = os.path.dirname(CARPETA_ACTUAL)
CARPETA_CONCEPTOS = os.path.join(CARPETA_PROYECTO, "conceptos")


def _forzar_utf8_consola():
    """La consola de Windows a veces usa cp1252 y revienta al imprimir
    simbolos matematicos (Omega, lambda, ⊨, etc). Forzamos UTF-8."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


_forzar_utf8_consola()


def ruta_pdf(nombre_archivo):
    """Busca el PDF primero en la carpeta del proyecto y luego en conceptos/."""
    candidatos = [
        os.path.join(CARPETA_PROYECTO, nombre_archivo),
        os.path.join(CARPETA_CONCEPTOS, nombre_archivo),
    ]
    for c in candidatos:
        if os.path.isfile(c):
            return c
    raise FileNotFoundError(f"No se encontro el PDF: {nombre_archivo}")


_LIGADURAS = {
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
    "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st",
}


def normalizar(texto):
    """Colapsa saltos de linea y espacios multiples para poder buscar una
    cita aunque el PDF la haya partido en varias lineas. Tambien deshace
    ligaduras tipograficas (fi, fl, ffi...) que muchos PDF academicos
    incrustan como un unico glifo distinto de sus letras sueltas."""
    for ligadura, plano in _LIGADURAS.items():
        texto = texto.replace(ligadura, plano)
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


_CACHE_TEXTO = {}


def texto_completo_pdf(nombre_archivo):
    """Extrae y cachea el texto completo (todas las paginas) de un PDF,
    junto con el texto normalizado de cada pagina por separado (para poder
    reportar en que pagina aparece cada cita)."""
    if nombre_archivo in _CACHE_TEXTO:
        return _CACHE_TEXTO[nombre_archivo]

    ruta = ruta_pdf(nombre_archivo)
    doc = fitz.open(ruta)
    paginas = [normalizar(p.get_text()) for p in doc]
    doc.close()
    completo = " ".join(paginas)
    _CACHE_TEXTO[nombre_archivo] = (completo, paginas)
    return completo, paginas


def buscar_cita(nombre_archivo, cita):
    """Busca 'cita' (substring, sin distinguir mayusculas) dentro del PDF.
    Devuelve dict con si se encontro, en que pagina (1-index) y el contexto
    real (150 caracteres alrededor) tal como esta en el PDF."""
    completo, paginas = texto_completo_pdf(nombre_archivo)
    cita_norm = normalizar(cita)
    pos = completo.lower().find(cita_norm.lower())
    resultado = {
        "archivo": nombre_archivo,
        "cita_buscada": cita,
        "encontrada": pos != -1,
        "pagina": None,
        "contexto": None,
    }
    if pos == -1:
        return resultado

    # localizar la pagina real donde cae esa posicion
    acumulado = 0
    for i, pag in enumerate(paginas):
        # +1 por el espacio separador que se agrega al unir paginas
        limite = acumulado + len(pag) + 1
        if pos < limite:
            resultado["pagina"] = i + 1
            break
        acumulado = limite

    ini = max(0, pos - 60)
    fin = min(len(completo), pos + len(cita_norm) + 90)
    resultado["contexto"] = completo[ini:fin]
    return resultado


def verificar_ausencia(nombre_archivo, frase):
    """Confirma que una frase (que contradiria la respuesta correcta) NO
    aparece en el PDF -o si aparece, lo reporta-, para descartar
    distractores por falsacion (criterio popperiano: intentar refutar,
    no solo confirmar)."""
    completo, _ = texto_completo_pdf(nombre_archivo)
    presente = normalizar(frase).lower() in completo.lower()
    return presente


def imprimir_encabezado(numero, enunciado):
    print("=" * 78)
    print(f"PREGUNTA {numero}")
    print("-" * 78)
    print(enunciado.strip())
    print("=" * 78)


def imprimir_alternativas(alternativas):
    for letra, texto in alternativas.items():
        print(f"  {letra}) {texto}")
    print()


def imprimir_evidencia(ev, indice=None):
    prefijo = f"[Evidencia {indice}] " if indice is not None else ""
    if ev["encontrada"]:
        print(f"{prefijo}CITA ENCONTRADA en '{ev['archivo']}' (pagina {ev['pagina']}):")
        print(f"    \"...{ev['contexto']}...\"")
    else:
        print(f"{prefijo}*** CITA NO ENCONTRADA en '{ev['archivo']}' *** -> {ev['cita_buscada']!r}")
    print()


def veredicto_final(letra_correcta, letra_esperada_txt, evidencias_ok):
    print("-" * 78)
    if not evidencias_ok:
        print("RESULTADO: NO CONFIRMADO -> al menos una cita no se encontro en el PDF "
              "original. No se puede validar cientificamente esta respuesta con la "
              "evidencia disponible.")
        return False
    if letra_correcta == letra_esperada_txt:
        print(f"RESULTADO: CONFIRMADO -> la evidencia textual/numerica respalda la "
              f"opcion ({letra_correcta}), que coincide con 'respuestas_examen_"
              f"verificadas.txt' ({letra_esperada_txt}).")
        return True
    else:
        print(f"RESULTADO: DISCREPANCIA -> la evidencia respalda ({letra_correcta}) "
              f"pero el txt de respuestas indica ({letra_esperada_txt}). Revisar.")
        return False
