"""Recrea el paquete local de fuentes y el catálogo para videos."""

from collections import Counter
from pathlib import Path
from shutil import copy2, copytree
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import fitz
from openpyxl import load_workbook


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MATERIAL = HERE / "material_curso"
MATERIAL.mkdir(exist_ok=True)

SOURCE_FILES = [
    "02_tema1_fundamentos_y_preparacion_datos.txt",
    "03_tema2_validacion_y_metricas.txt",
    "04_tema3_extraccion_caracteristicas.txt",
    "05_tema4_modelos_regresion.txt",
    "06_tema5_modelos_clasificacion.txt",
    "07_explicacion_profunda_por_bloques.md",
    "08_aprendizaje_supervisado_desde_cero.md",
    "prompt_tutor_chat_v11.md",
]
WORKBOOK = "Seguimiento_Aprendizaje_Supervisado_mejorado.xlsx"

for name in SOURCE_FILES:
    copy2(ROOT / name, MATERIAL / name)
copy2(ROOT / "outputs" / "explicacion_excel" / WORKBOOK, MATERIAL / WORKBOOK)

CLASSES = ROOT.parent
PDF = "05MIAR_GAsencio_nueva_imagen.pdf"
PPTX = "Tema 3 - Extracción de características.pptx"
copy2(CLASSES / PDF, MATERIAL / PDF)
copy2(CLASSES / PPTX, MATERIAL / PPTX)
copytree(CLASSES / "viu_aprendizaje_supervisado-main", MATERIAL / "notebooks_y_recursos", dirs_exist_ok=True)

# Texto consultable por página y diapositiva. El PDF y el PPTX originales se
# conservan porque fórmulas, imágenes y disposición pueden perderse al extraer.
manual = fitz.open(MATERIAL / PDF)
pdf_lines = ["# Texto extraído del manual PDF", "", "Consulta el PDF original para figuras, fórmulas y disposición. Este archivo solo facilita buscar texto.", ""]
for i, page in enumerate(manual, 1):
    pdf_lines += [f"## Página PDF {i}", "", page.get_text().strip(), ""]
(MATERIAL / "MANUAL_PDF_TEXTO.md").write_text("\n".join(pdf_lines), encoding="utf-8")

with ZipFile(MATERIAL / PPTX) as archive:
    slides = sorted(
        [name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
        key=lambda name: int(re.search(r"slide(\d+)", name).group(1)),
    )
    ppt_lines = ["# Texto extraído del PowerPoint del tema 3", "", "Consulta el PPTX original para gráficos, fórmulas y distribución visual. Este archivo solo facilita buscar texto.", ""]
    for i, name in enumerate(slides, 1):
        root = ET.fromstring(archive.read(name))
        texts = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
        ppt_lines += [f"## Diapositiva {i}", "", " ".join(texts).strip(), ""]
(MATERIAL / "TEMA3_PPTX_TEXTO.md").write_text("\n".join(ppt_lines), encoding="utf-8")

sheet = load_workbook(MATERIAL / WORKBOOK, read_only=True, data_only=False)["Mapa de estudio"]
rows = list(sheet.values)[1:]
assert len(rows) == 185, f"Se esperaban 185 conceptos; hay {len(rows)}"


def one_line(value):
    return " ".join(str(value or "").split()).replace("|", "\\|")


lines = [
    "# Catálogo completo de conceptos para videos",
    "",
    "Fuente del orden, los nombres originales, los estados y las explicaciones sencillas: `material_curso/Seguimiento_Aprendizaje_Supervisado_mejorado.xlsx`, hoja `Mapa de estudio`. Cada ficha conserva el código del curso. Para producir un video, consulta también la fuente íntegra indicada; este catálogo es un mapa pedagógico y no sustituye la fuente.",
    "",
    "**Alcance:** cinco bloques, veintinueve temas de nivel 1 y ciento cincuenta y un conceptos de nivel 2. Los cinco encabezados de bloque completan las ciento ochenta y cinco filas. Los estados son los que estaban registrados en el Excel; no se deducen del texto de este catálogo.",
    "",
    "**Fuentes originales integradas:** manual PDF, PowerPoint de tema 3 y repositorio de notebooks y recursos. Los archivos de texto extraído ayudan a buscar; para fórmulas, figuras y código consulta siempre los originales. La teoría detallada de SVM no se identificó en el resumen `06`; si tampoco consta en el manual, marca ese límite en lugar de completarlo con suposiciones.",
    "",
    "**Excepción de estructura:** `3.4` no tiene filas de nivel 2 en el Excel. Explícalo como un único segmento de nivel 1; el cero en el índice no significa que se omita.",
    "",
    "## Índice de videos",
    "",
    "| Video | Tema original | Segmentos de nivel 2 | Estado previo | Fuente de consulta |",
    "|---|---|---:|---|---|",
]

for row in rows:
    code, _, title, level, status, explanation, next_step, _, _, source = row[:10]
    if level == 1:
        n = sum(
            1 for other in rows
            if other[3] == 2 and str(other[0]).startswith(str(code) + ".")
        )
        source_name = {
            "1": SOURCE_FILES[0], "2": SOURCE_FILES[1],
            "3": SOURCE_FILES[2], "4": SOURCE_FILES[3],
            "5": SOURCE_FILES[4],
        }[str(code).split(".")[0]]
        display_source = (f"`material_curso/{PPTX}` y `material_curso/{SOURCE_FILES[2]}`"
                          if str(code).startswith("3.") else f"`material_curso/{source_name}`")
        lines.append(
            f"| `{code}` | {one_line(title)} | {n} | {one_line(status)} | "
            f"{display_source} |"
        )

lines += [
    "",
    "## Fichas en el orden del curso",
    "",
    "**Cómo leerlas:** nivel 0 = bloque; nivel 1 = tema para un video; nivel 2 = concepto para un segmento con una sola pregunta de comprensión y un caso nuevo de aplicación. Si un tema de nivel 1 no tiene hijos de nivel 2, ese mismo tema forma un segmento. Una explicación sencilla ayuda a empezar, pero cualquier fórmula, cifra, procedimiento o límite debe cotejarse con la fuente íntegra.",
    "",
]

for row in rows:
    code, _, title, level, status, explanation, next_step, _, _, source = row[:10]
    heading = {0: "##", 1: "###", 2: "####"}[level]
    lines += [
        f"{heading} {code} {one_line(title)}",
        "",
        f"- **Nivel:** {level}. **Estado registrado:** {one_line(status)}.",
        f"- **Explicación sencilla:** {one_line(explanation)}",
    ]
    if next_step:
        lines.append(f"- **Siguiente aplicación sugerida:** {one_line(next_step)}")
    if str(code).startswith("3"):
        lines.append(
            f"- **Fuentes originales:** `material_curso/{PPTX}` para teoría y figuras; "
            "`material_curso/04_tema3_extraccion_caracteristicas.txt` para el resumen de prácticas; "
            "`material_curso/notebooks_y_recursos/tema3/` para código."
        )
        lines.append(f"- **Referencia original del Excel:** {one_line(source)}. "
                     "Busca la diapositiva indicada en el PPTX original, no solo en el texto extraído.")
    else:
        lines.append(f"- **Fuente íntegra:** `material_curso/{one_line(source)}`.")
        lines.append(f"- **Fuente primaria adicional:** `material_curso/{PDF}` y notebooks del bloque en `material_curso/notebooks_y_recursos/`.")
    if str(code).startswith("5.3"):
        lines.append("- **Límite:** la teoría detallada de SVM no consta en la fuente local; verifica el flujo de `SVC` y no inventes los mecanismos faltantes.")
    if str(code) == "3.8.c":
        lines.append("- **Errata comprobada:** la diapositiva 35 del PPTX define extensión como proporción entre el área de la región y su *bounding box*, y más abajo atribuye un cociente de esas áreas al diámetro de Feret. Consulta `ERRATAS_Y_LIMITES.md`; no enseñes ese cociente como diámetro verificado.")
    lines.append("")

out = HERE / "CATALOGO_COMPLETO_PARA_VIDEOS.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
counts = Counter(row[3] for row in rows)
print(f"Integrados {len(SOURCE_FILES) + 3} archivos base, manual, diapositivas y repositorio; catálogo con {len(rows)} fichas y niveles {dict(counts)}: {out}")
