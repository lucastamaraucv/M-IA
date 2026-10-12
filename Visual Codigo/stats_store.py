#!/usr/bin/env python3
"""Espejo en SQLite (normalizado a 3FN) de las estadísticas de quiz que el
navegador ya lleva en localStorage (`_stats` en core.js) — localStorage
resuelve la app en vivo, pero no es consultable fuera del navegador ni
apto para un reporte histórico. Aquí se guarda el detalle real evento a
evento (cada intento es una fila), no contadores ya sumados, para que el
diseño sea normalizado de verdad: fails/dontKnow/sureCount no se guardan
como columnas — se DERIVAN con SQL a partir de `attempts` en get_report().

Esquema (3FN):
  topics(topic_id PK, mode, topic_idx, name)            UNIQUE(mode, topic_idx)
    -- name depende de (mode, topic_idx), no de nada más.
  attempts(attempt_id PK, topic_id FK, result, confidence, created_at)
    -- cada columna depende solo de attempt_id (la clave), no entre sí.
  leitner_state(topic_id PK/FK, box, due_at, updated_at)
    -- estado ACTUAL (no evento), una fila por tema, se sobreescribe.
Ningún dato derivable (conteos, promedios) se almacena — se calcula al leer.
"""
import os as _os
import sqlite3 as _sqlite3
import datetime as _datetime

DB_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'student_notes.db')


def _get_conn():
    conn = _sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            topic_idx INTEGER NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(mode, topic_idx)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL REFERENCES topics(topic_id),
            result TEXT NOT NULL CHECK(result IN ('correct','incorrect','dont_know')),
            confidence TEXT CHECK(confidence IN ('sure','unsure','guess') OR confidence IS NULL),
            created_at TEXT NOT NULL
        )
    ''')
    # Migración aditiva: doubted_option/reason_tag se agregaron después de que
    # CREATE TABLE IF NOT EXISTS ya hubiera creado la tabla en instalaciones
    # existentes -- ADD COLUMN es la única forma de retrofitarla sin perder
    # las filas ya guardadas. OperationalError = la columna ya existe.
    for _col_sql in ('ALTER TABLE attempts ADD COLUMN doubted_option TEXT',
                      'ALTER TABLE attempts ADD COLUMN reason_tag TEXT'):
        try:
            conn.execute(_col_sql)
        except _sqlite3.OperationalError:
            pass
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leitner_state (
            topic_id INTEGER PRIMARY KEY REFERENCES topics(topic_id),
            box INTEGER NOT NULL,
            due_at TEXT,
            updated_at TEXT NOT NULL
        )
    ''')
    return conn


def _get_or_create_topic(conn, mode, topic_idx, name):
    row = conn.execute('SELECT topic_id FROM topics WHERE mode=? AND topic_idx=?', (mode, topic_idx)).fetchone()
    if row:
        if name:
            conn.execute('UPDATE topics SET name=? WHERE topic_id=?', (name, row[0]))
        return row[0]
    cur = conn.execute('INSERT INTO topics (mode, topic_idx, name) VALUES (?, ?, ?)', (mode, topic_idx, name or f'{mode}#{topic_idx}'))
    return cur.lastrowid


def _upsert_leitner(conn, topic_id, box, due_at):
    now = _datetime.datetime.now().isoformat(timespec='seconds')
    conn.execute('''
        INSERT INTO leitner_state (topic_id, box, due_at, updated_at) VALUES (?, ?, ?, ?)
        ON CONFLICT(topic_id) DO UPDATE SET box=excluded.box, due_at=excluded.due_at, updated_at=excluded.updated_at
    ''', (topic_id, box, due_at, now))


def record_attempt(mode, topic_idx, topic_name, result, box=None, due_at=None):
    """Un intento nuevo (correct/incorrect/dont_know) -- confidence se agrega
    después con record_confidence() si aplica (solo tras un acierto)."""
    if result not in ('correct', 'incorrect', 'dont_know'):
        return None
    conn = _get_conn()
    try:
        topic_id = _get_or_create_topic(conn, mode, topic_idx, topic_name)
        cur = conn.execute(
            'INSERT INTO attempts (topic_id, result, confidence, created_at) VALUES (?, ?, NULL, ?)',
            (topic_id, result, _datetime.datetime.now().isoformat(timespec='seconds')),
        )
        if box is not None:
            _upsert_leitner(conn, topic_id, box, due_at)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def record_confidence(mode, topic_idx, level, box=None, due_at=None):
    """Actualiza el intento CORRECTO más reciente de este tema que todavía
    no tenga confidence asignado -- confidence es un atributo del propio
    intento (evento), no una entidad aparte."""
    if level not in ('sure', 'unsure', 'guess'):
        return False
    conn = _get_conn()
    try:
        topic_row = conn.execute('SELECT topic_id FROM topics WHERE mode=? AND topic_idx=?', (mode, topic_idx)).fetchone()
        if not topic_row:
            return False
        topic_id = topic_row[0]
        row = conn.execute('''
            SELECT attempt_id FROM attempts
            WHERE topic_id=? AND result='correct' AND confidence IS NULL
            ORDER BY attempt_id DESC LIMIT 1
        ''', (topic_id,)).fetchone()
        if not row:
            return False
        conn.execute('UPDATE attempts SET confidence=? WHERE attempt_id=?', (level, row[0]))
        if box is not None:
            _upsert_leitner(conn, topic_id, box, due_at)
        conn.commit()
        return True
    finally:
        conn.close()


def record_reasoning(mode, topic_idx, doubted_option, reason_tag):
    """Motivo (botones, sin texto libre) del intento MÁS RECIENTE de este
    tema, sin importar si acertó o falló -- a diferencia de confidence, que
    solo aplica tras un acierto, el razonamiento se pide siempre."""
    conn = _get_conn()
    try:
        topic_row = conn.execute('SELECT topic_id FROM topics WHERE mode=? AND topic_idx=?', (mode, topic_idx)).fetchone()
        if not topic_row:
            return False
        topic_id = topic_row[0]
        row = conn.execute(
            'SELECT attempt_id FROM attempts WHERE topic_id=? ORDER BY attempt_id DESC LIMIT 1',
            (topic_id,),
        ).fetchone()
        if not row:
            return False
        conn.execute('UPDATE attempts SET doubted_option=?, reason_tag=? WHERE attempt_id=?',
                     (doubted_option, reason_tag, row[0]))
        conn.commit()
        return True
    finally:
        conn.close()


def get_reasoning_signal(mode, topic_idxs):
    """Filas recientes con motivo/duda registrados para un bloque de temas
    -- la señal cruda que se le pasa a Claude para diagnosticar un patrón
    real de confusión, no solo aciertos/fallos sueltos."""
    if not topic_idxs:
        return []
    conn = _get_conn()
    try:
        placeholders = ','.join('?' * len(topic_idxs))
        rows = conn.execute(f'''
            SELECT t.name, a.result, a.doubted_option, a.reason_tag, a.created_at
            FROM attempts a JOIN topics t ON t.topic_id = a.topic_id
            WHERE t.mode=? AND t.topic_idx IN ({placeholders}) AND a.reason_tag IS NOT NULL
            ORDER BY a.created_at DESC LIMIT 30
        ''', (mode, *topic_idxs)).fetchall()
        return [{'topic': r[0], 'result': r[1], 'doubted': r[2], 'reason_tag': r[3], 'at': r[4]} for r in rows]
    finally:
        conn.close()


def get_report(mode=None):
    """Reporte agregado por tema -- todos los conteos se DERIVAN con SQL a
    partir de `attempts`, no se guardan como columnas (evita redundancia)."""
    conn = _get_conn()
    try:
        where = 'WHERE t.mode = ?' if mode else ''
        params = (mode,) if mode else ()
        rows = conn.execute(f'''
            SELECT
                t.mode, t.topic_idx, t.name,
                COUNT(*) FILTER (WHERE a.result='correct') AS correct,
                COUNT(*) FILTER (WHERE a.result='incorrect') AS incorrect,
                COUNT(*) FILTER (WHERE a.result='dont_know') AS dont_know,
                COUNT(*) FILTER (WHERE a.confidence='sure') AS sure,
                COUNT(*) FILTER (WHERE a.confidence='unsure') AS unsure,
                COUNT(*) FILTER (WHERE a.confidence='guess') AS guess,
                COUNT(*) AS total,
                MAX(a.created_at) AS last_attempt,
                l.box, l.due_at
            FROM topics t
            JOIN attempts a ON a.topic_id = t.topic_id
            LEFT JOIN leitner_state l ON l.topic_id = t.topic_id
            {where}
            GROUP BY t.topic_id
            ORDER BY t.mode, t.topic_idx
        ''', params).fetchall()
        cols = ['mode', 'topic_idx', 'name', 'correct', 'incorrect', 'dont_know',
                'sure', 'unsure', 'guess', 'total', 'last_attempt', 'box', 'due_at']
        out = []
        for r in rows:
            d = dict(zip(cols, r))
            # "puntuacion de debilidad": cuanto mas alta, mas urge repasar --
            # se calcula aqui (no se guarda) para no duplicar el dato.
            d['weakness'] = d['incorrect'] * 2 + d['dont_know'] * 3 + d['guess'] * 1
            out.append(d)
        return out
    finally:
        conn.close()


def get_trend(mode=None, days=14):
    """% de acierto por día, últimos `days` días (con datos) -- para el
    mini-gráfico de tendencia del reporte. Se agrupa por DATE(created_at),
    derivado de `attempts`, igual que get_report() (nada se guarda ya
    resumido)."""
    conn = _get_conn()
    try:
        where = 'WHERE t.mode = ?' if mode else ''
        params = (mode,) if mode else ()
        rows = conn.execute(f'''
            SELECT
                date(a.created_at) AS day,
                COUNT(*) FILTER (WHERE a.result='correct') AS correct,
                COUNT(*) AS total
            FROM attempts a
            JOIN topics t ON t.topic_id = a.topic_id
            {where}
            GROUP BY day
            ORDER BY day DESC
            LIMIT ?
        ''', params + (days,)).fetchall()
        out = [{'day': r[0], 'correct': r[1], 'total': r[2],
                'pct': round(r[1] / r[2] * 100) if r[2] else 0} for r in rows]
        out.reverse()  # cronologico, mas viejo primero (para dibujar de izquierda a derecha)
        return out
    finally:
        conn.close()


def get_streak():
    """Días consecutivos (hasta hoy o ayer) con al menos un intento
    guardado, en CUALQUIER curso -- se deriva de las fechas distintas en
    `attempts`, no se guarda un contador aparte."""
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT DISTINCT date(created_at) AS day FROM attempts ORDER BY day DESC").fetchall()
        days = [r[0] for r in rows]
        if not days:
            return 0
        today = _datetime.date.today()
        streak = 0
        cursor = today
        day_set = set(days)
        # si hoy todavia no hay intento, el conteo arranca en ayer (no se
        # rompe la racha solo por no haber estudiado TODAVIA hoy)
        if str(cursor) not in day_set:
            cursor = cursor - _datetime.timedelta(days=1)
        while str(cursor) in day_set:
            streak += 1
            cursor = cursor - _datetime.timedelta(days=1)
        return streak
    finally:
        conn.close()
