#!/usr/bin/env python3
"""Guarda en SQLite lo que el alumno escribe en "Autoexplícate" (AO/RA/AS)
cuando pide guardarlo — a diferencia del resto del progreso de la app
(localStorage del navegador, ver core.js), esto vive en un archivo real en
disco: sobrevive a borrar el caché del navegador, es legible fuera de la
app, y es la única forma de que quede algo que se pueda revisar más tarde
(localStorage no es accesible desde fuera del navegador)."""
import os as _os
import sqlite3 as _sqlite3
import datetime as _datetime

DB_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'student_notes.db')


def _get_conn():
    conn = _sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            topic_idx INTEGER,
            topic_name TEXT,
            text TEXT NOT NULL,
            feedback TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    # Migración aditiva (2026-08-13, peldaño Transferencia de la Escalera de
    # Dominio): 'kind' distingue una nota/duda normal ('note', el uso de
    # siempre) de una pregunta de transferencia que el propio alumno inventó
    # ('transfer', nivel 7 de su plan de aprendizaje: "resolver un problema
    # nuevo donde no aparece explícitamente el nombre del concepto"). Mismo
    # patrón ADD COLUMN que doubted_option/reason_tag en stats_store.py.
    try:
        conn.execute("ALTER TABLE notes ADD COLUMN kind TEXT DEFAULT 'note'")
    except _sqlite3.OperationalError:
        pass
    return conn


def save_note(mode, topic_idx, topic_name, text, feedback=None, kind='note'):
    text = (text or '').strip()
    if not text:
        return None
    conn = _get_conn()
    try:
        cur = conn.execute(
            'INSERT INTO notes (mode, topic_idx, topic_name, text, feedback, created_at, kind) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (mode, topic_idx, topic_name, text, feedback, _datetime.datetime.now().isoformat(timespec='seconds'), kind or 'note'),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_notes(mode=None, limit=200):
    conn = _get_conn()
    try:
        if mode:
            rows = conn.execute(
                'SELECT id, mode, topic_idx, topic_name, text, feedback, created_at, kind FROM notes WHERE mode=? ORDER BY id DESC LIMIT ?',
                (mode, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT id, mode, topic_idx, topic_name, text, feedback, created_at, kind FROM notes ORDER BY id DESC LIMIT ?',
                (limit,),
            ).fetchall()
        cols = ['id', 'mode', 'topic_idx', 'topic_name', 'text', 'feedback', 'created_at', 'kind']
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()
