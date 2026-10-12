import json
with open('01MIAR_ACT_WhitePapers.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']
esperados = {
    9:  ('mark', '1. Referencia'),
    10: ('mark', '2. Por qu'),
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
for idx, (tipo, keyword) in esperados.items():
    actual_tipo = cells[idx]['cell_type'][:4]
    primeros60 = ''.join(cells[idx]['source'])[:60]
    tipo_ok = actual_tipo == tipo[:4]
    kw_ok = (keyword is None) or (keyword in primeros60)
    estado = "OK" if (tipo_ok and kw_ok) else "FALLA"
    print(f"Celda {idx}: [{estado}] tipo={actual_tipo}(exp:{tipo[:4]}) kw_ok={kw_ok} | '{primeros60[:50]}'")
