"""Auditoria completa contra la rubrica de la actividad."""
import json, re

with open('01MIAR_ACT_WhitePapers.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

def src(i): return ''.join(cells[i]['source'])
def tiene(i, kw): return kw.lower() in src(i).lower()

OK = "  [OK]"
WARN = "  [!] "

print("=" * 65)
print("AUDITORIA RUBRICA — 01MIAR Actividad WhitePapers")
print("=" * 65)

# ── ESTILO (20%) ─────────────────────────────────────────────────────────────
print("\n[ESTILO 20%]")

# Celda 8: header alumno. Celdas 9-11: secciones 1-3. Celda 12: seccion 4.
# Celdas 13-15: codigo. Celda 16: seccion 5. Celdas 17-18: 6-7. Celda 19: refs.
esperados = {
    9:  ('mark', '1. Referencia'),
    10: ('mark', '2.'),
    11: ('mark', '3. Resumen'),
    12: ('mark', '4. Ejemplo'),
    13: ('code', None),
    14: ('code', None),
    15: ('code', None),
    16: ('mark', '5. Explicaci'),
    17: ('mark', '6. Mirada'),
    18: ('mark', '7. Conclusi'),
    19: ('mark', 'Referencias'),
}
ok_orden = True
for idx, (tipo, keyword) in esperados.items():
    if idx >= len(cells):
        ok_orden = False; continue
    if cells[idx]['cell_type'][:4] != tipo[:4]:
        ok_orden = False
    if keyword and keyword not in ''.join(cells[idx]['source'])[:60]:
        ok_orden = False

print(f"{OK if ok_orden else WARN} Estructura: secciones 1-7 + codigo en orden correcto")

dup = sum(1 for c in cells if c['cell_type'] == 'markdown' and '5. Explicaci' in ''.join(c['source']))
print(f"{OK if dup == 1 else WARN} Sin secciones duplicadas (Seccion 5 aparece {dup} vez/veces)")

tiene_ieee = tiene(9, 'Proc.') and tiene(9, 'ICLR')
print(f"{OK if tiene_ieee else WARN} Referencia en formato IEEE con datos completos")

code_cells = [c for c in cells if c['cell_type'] == 'code']
con_outputs = sum(1 for c in code_cells if c.get('outputs'))
print(f"{OK if con_outputs >= 3 else WARN} Celdas de codigo con outputs ejecutados: {con_outputs}/3")

# ── ARTICULO (20%) ───────────────────────────────────────────────────────────
print("\n[ARTICULO 20%]")

tiene_arxiv = any(tiene(i, '2503.05108') or tiene(i, 'ICLR 2025') for i in range(9, 20))
print(f"{OK if tiene_arxiv else WARN} Articulo identificado: arXiv 2503.05108 / ICLR 2025")

tiene_python = any(tiene(i, 'Python') and tiene(i, 'NumPy') for i in range(9, 20))
print(f"{OK if tiene_python else WARN} Relacion con Python/librerias explicada")

tiene_2025 = any('2025' in src(i) for i in range(9, 20))
print(f"{OK if tiene_2025 else WARN} Publicacion posterior a 2024 (ICLR 2025)")

tiene_pares = any(tiene(i, 'pares') or tiene(i, 'ICLR') for i in range(9, 20))
print(f"{OK if tiene_pares else WARN} Relevancia academica (revision por pares)")

# ── CONTENIDOS (60%) ─────────────────────────────────────────────────────────
print("\n[CONTENIDOS 60%]")

tiene_justif = tiene(10, 'por qu') and tiene(10, 'usabilidad')
print(f"{OK if tiene_justif else WARN} Seccion 2: justificacion + usabilidad")

tiene_personal = any(p in src(10) for p in ['quiero', 'me interesa', 'me llama', 'busco'])
print(f"{OK if tiene_personal else WARN} Seccion 2: perspectiva personal")

tiene_resumen = tiene(11, 'LIF') and tiene(11, 'compartimento') and tiene(11, 'frecuencia')
print(f"{OK if tiene_resumen else WARN} Seccion 3: resumen cubre propuesta tecnica")

tiene_resultados = tiene(11, 'RSE') or tiene(11, 'Tabla') or tiene(11, 'R^2')
print(f"{OK if tiene_resultados else WARN} Seccion 3: menciona resultados del paper")

tiene_eq5 = any(tiene(i, 'Ecuaci') and tiene(i, 'LIF') for i in [12, 13, 16])
print(f"{OK if tiene_eq5 else WARN} Seccion 4: ejemplo referencia Ecuacion 5")

tiene_datos_reales = any(tiene(i, 'UCI') or tiene(i, 'electricity') for i in [12, 16])
print(f"{OK if tiene_datos_reales else WARN} Seccion 4: se usan datos reales del paper")

tiene_expl = len(src(16)) > 1000
print(f"{OK if tiene_expl else WARN} Seccion 5: explicacion completa ({len(src(16))} chars)")

expl_ok = (tiene(16, 'dendrita') and tiene(16, 'soma') and
           tiene(16, 'FFT') and tiene(16, 'ganancia') and tiene(16, 'estabilidad'))
print(f"{OK if expl_ok else WARN} Seccion 5: cubre dendrita/soma, FFT, ganancia, estabilidad")

# La explicacion describe datos reales, no sinteticos
expl_real = tiene(16, 'nodo 0') and tiene(16, 'CSV')
print(f"{OK if expl_real else WARN} Seccion 5: describe dataset real (nodo 0 del CSV)")

expl_no_sintetica = 'periodo 120' not in src(16) and 'onda lenta' not in src(16)
print(f"{OK if expl_no_sintetica else WARN} Seccion 5: no menciona señal sintetica antigua")

tiene_critica = tiene(17, 'limite') or tiene(17, 'asterisco') or tiene(17, 'conviene')
print(f"{OK if tiene_critica else WARN} Seccion 6: mirada critica sobre limites del paper")

tiene_conclusion = tiene(18, 'aprend') and len(src(18)) > 400
print(f"{OK if tiene_conclusion else WARN} Seccion 7: conclusion con reflexion personal")

# ── NOTA DATASET ─────────────────────────────────────────────────────────────
print("\n[DATASET — nota en seccion 4]")
nota_real = tiene(12, 'datos reales') or tiene(12, 'reales, no sint')
print(f"{OK if nota_real else WARN} Nota aclara que son datos reales UCI")

# "sintetico" aparece solo negado, no como afirmacion
s12 = src(12).lower()
# busca "sintetico" sin "no" delante
sintetico_afirmado = bool(re.search(r'(?<!no )(sint.tico)', s12))
print(f"{OK if not sintetico_afirmado else WARN} No afirma que el dataset es sintetico")

# ── OUTPUTS ──────────────────────────────────────────────────────────────────
print("\n[OUTPUTS DE LAS CELDAS DE CODIGO]")
for i, c in enumerate(cells):
    if c['cell_type'] == 'code' and c.get('outputs'):
        n_img = sum(1 for o in c['outputs'] if 'image/png' in o.get('data', {}))
        n_txt = sum(1 for o in c['outputs'] if o.get('output_type') == 'stream')
        print(f"  Celda {i}: {len(c['outputs'])} outputs | {n_img} imagen(es) | {n_txt} texto(s)")

# ── NUMEROS CLAVE DEL PAPER ───────────────────────────────────────────────────
print("\n[NUMEROS CLAVE — coincidencia con Sec. 4.4 del paper]")
txt16 = [o for c in cells if c['cell_type'] == 'code'
         for o in c.get('outputs', []) if o.get('output_type') == 'stream']
texto_outputs = ' '.join(''.join(o.get('text', [])) for o in txt16)
for numero, descripcion in [('0.700', 'ganancia dendrita T=120'), ('0.026', 'ganancia dendrita T=4'),
                              ('0.698', 'ganancia soma T=120'),   ('0.925', 'ganancia soma T=4')]:
    encontrado = numero in texto_outputs
    print(f"  {OK if encontrado else WARN} {numero} ({descripcion})")

print("\n" + "=" * 65)
print("FIN AUDITORIA — todo OK = listo para entregar")
