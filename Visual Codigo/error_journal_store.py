#!/usr/bin/env python3
"""Cuaderno de errores personal: cada vez que el alumno falla una pregunta
de opción múltiple con `whyNot` (AO/RA/AS/Repaso mezclado), el frontend
guarda aquí automáticamente PROBLEMA/MI RESPUESTA/CONCEPTO CORRECTO/CAUSA
(ver core.js, _logErrorJournal). La REGLA PERSONAL la escribe el alumno
después, con calma, revisando el cuaderno — no en caliente durante el
estudio. Mismo patrón que notes_store.py: SQLite en disco, sobrevive a
borrar el caché del navegador."""
import os as _os
import sqlite3 as _sqlite3
import datetime as _datetime

DB_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'student_notes.db')


def _get_conn():
    conn = _sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS error_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            topic_idx INTEGER,
            topic_name TEXT,
            question TEXT NOT NULL,
            chosen_text TEXT,
            correct_text TEXT,
            why_wrong TEXT,
            personal_rule TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    return conn


def save_error(mode, topic_idx, topic_name, question, chosen_text, correct_text, why_wrong):
    question = (question or '').strip()
    if not question:
        return None
    conn = _get_conn()
    try:
        cur = conn.execute(
            'INSERT INTO error_journal (mode, topic_idx, topic_name, question, chosen_text, correct_text, why_wrong, personal_rule, created_at) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (mode, topic_idx, topic_name, question, chosen_text, correct_text, why_wrong, None,
             _datetime.datetime.now().isoformat(timespec='seconds')),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_errors(mode=None, limit=200):
    conn = _get_conn()
    try:
        if mode:
            rows = conn.execute(
                'SELECT id, mode, topic_idx, topic_name, question, chosen_text, correct_text, why_wrong, personal_rule, created_at '
                'FROM error_journal WHERE mode=? ORDER BY id DESC LIMIT ?',
                (mode, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT id, mode, topic_idx, topic_name, question, chosen_text, correct_text, why_wrong, personal_rule, created_at '
                'FROM error_journal ORDER BY id DESC LIMIT ?',
                (limit,),
            ).fetchall()
        cols = ['id', 'mode', 'topic_idx', 'topic_name', 'question', 'chosen_text', 'correct_text', 'why_wrong', 'personal_rule', 'created_at']
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def update_personal_rule(error_id, personal_rule):
    conn = _get_conn()
    try:
        conn.execute('UPDATE error_journal SET personal_rule=? WHERE id=?', (personal_rule, error_id))
        conn.commit()
        return conn.total_changes > 0
    finally:
        conn.close()
