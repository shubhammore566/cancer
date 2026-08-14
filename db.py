"""
db.py
Handles all SQLite persistence for patients and their diagnosis history.
"""
import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "patient_data", "clinic.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            prediction TEXT,
            confidence REAL,
            original_image_path TEXT,
            deblurred_image_path TEXT,
            gradcam_image_path TEXT,
            doctor_notes TEXT,
            created_at TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    """)
    conn.commit()
    conn.close()


def add_patient(name, age, gender, contact, notes=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO patients (name, age, gender, contact, notes, created_at) VALUES (?,?,?,?,?,?)",
        (name, age, gender, contact, notes, datetime.datetime.now().isoformat()),
    )
    conn.commit()
    patient_id = cur.lastrowid
    conn.close()
    return patient_id


def get_all_patients():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM patients ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows


def get_patient(patient_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return row


def delete_patient(patient_id):
    conn = get_connection()
    conn.execute("DELETE FROM diagnoses WHERE patient_id = ?", (patient_id,))
    conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()


def add_diagnosis(patient_id, prediction, confidence, original_image_path,
                   deblurred_image_path, gradcam_image_path, doctor_notes=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO diagnoses
        (patient_id, prediction, confidence, original_image_path, deblurred_image_path,
         gradcam_image_path, doctor_notes, created_at)
        VALUES (?,?,?,?,?,?,?,?)
    """, (patient_id, prediction, confidence, original_image_path, deblurred_image_path,
          gradcam_image_path, doctor_notes, datetime.datetime.now().isoformat()))
    conn.commit()
    diag_id = cur.lastrowid
    conn.close()
    return diag_id


def get_diagnoses_for_patient(patient_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM diagnoses WHERE patient_id = ? ORDER BY created_at DESC",
        (patient_id,)
    ).fetchall()
    conn.close()
    return rows


def get_diagnosis(diagnosis_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM diagnoses WHERE id = ?", (diagnosis_id,)).fetchone()
    conn.close()
    return row


def get_all_diagnoses_with_patient():
    conn = get_connection()
    rows = conn.execute("""
        SELECT d.*, p.name as patient_name, p.age as patient_age, p.gender as patient_gender
        FROM diagnoses d JOIN patients p ON d.patient_id = p.id
        ORDER BY d.created_at DESC
    """).fetchall()
    conn.close()
    return rows
