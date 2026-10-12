"""Plantillas reutilizables para celdas markdown coloreadas en .ipynb.
Las usamos para diferenciar visualmente:
  - TEORIA   (azul claro)
  - EJEMPLO  (gris claro)  -- opcional, normalmente las celdas de
                              codigo originales actuan como ejemplo
  - TU TURNO (amarillo / naranja)
  - SOLUCION SUGERIDA (verde claro)
  - DATO    (violeta) para apuntes secundarios
"""

def teoria(titulo, cuerpo_md):
    return (
        '<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;'
        'padding:12px 16px;border-radius:6px;margin:6px 0;">'
        f'<b style="color:#1864ab;font-size:14px;">TEORIA &middot; {titulo}</b>\n\n'
        f'{cuerpo_md}\n\n'
        '</div>'
    )


def tu_turno(numero, enunciado_md):
    return (
        '<div style="background-color:#fff9db;border-left:6px solid #f59f00;'
        'padding:12px 16px;border-radius:6px;margin:6px 0;">'
        f'<b style="color:#a05a00;font-size:14px;">TU TURNO {numero}</b>\n\n'
        f'{enunciado_md}\n\n'
        '<i>Escribe tu codigo en la celda que sigue.</i>'
        '</div>'
    )


def solucion_md(cuerpo_md):
    return (
        '<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;'
        'padding:12px 16px;border-radius:6px;margin:6px 0;">'
        '<b style="color:#1b5e20;font-size:14px;">SOLUCION SUGERIDA</b>\n\n'
        f'{cuerpo_md}\n\n'
        '</div>'
    )


def dato(cuerpo_md):
    return (
        '<div style="background-color:#f3f0ff;border-left:6px solid #7048e8;'
        'padding:12px 16px;border-radius:6px;margin:6px 0;">'
        '<b style="color:#4c2d9e;font-size:14px;">PARA RECORDAR</b>\n\n'
        f'{cuerpo_md}\n\n'
        '</div>'
    )


def aviso(cuerpo_md):
    return (
        '<div style="background-color:#fff0f0;border-left:6px solid #e03131;'
        'padding:12px 16px;border-radius:6px;margin:6px 0;">'
        '<b style="color:#7d1818;font-size:14px;">CUIDADO</b>\n\n'
        f'{cuerpo_md}\n\n'
        '</div>'
    )
