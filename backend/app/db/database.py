import sqlite3
import os
import uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.abspath(os.path.curdir), "sham_platform.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id TEXT PRIMARY KEY,
            user_id TEXT,
            email TEXT,
            plan TEXT,
            amount REAL,
            transaction_id TEXT,
            sender_account TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            license_key TEXT PRIMARY KEY,
            client_name TEXT,
            plan_type TEXT,
            expires_at TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            details TEXT,
            timestamp TEXT
        )
    ''')
    defaults = {
        "telegram_bot_token": "MOCK_BOT_TOKEN",
        "telegram_channel_id": "@ShamSignalsVIP",
        "shamcash_number": "09XXXXXXXX"
    }
    for k, v in defaults.items():
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
    conn.commit()
    conn.close()

def get_settings() -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM settings")
    res = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return {
        "telegram_bot_token": res.get("telegram_bot_token", "MOCK_BOT_TOKEN"),
        "telegram_channel_id": res.get("telegram_channel_id", "@ShamSignalsVIP"),
        "shamcash_number": res.get("shamcash_number", "09XXXXXXXX")
    }

def update_settings(new_settings: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for k, v in new_settings.items():
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (k, v))
    conn.commit()
    conn.close()

def log_audit(action: str, details: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)", 
                   (action, details, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def generate_client_license(client_name: str, plan_type: str) -> dict:
    key = "SHAM-LIC-" + str(uuid.uuid4())[:8].upper()
    expires = "2027-12-31"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO licenses (license_key, client_name, plan_type, expires_at, status) VALUES (?, ?, ?, ?, ?)",
                   (key, client_name, plan_type, expires, "ACTIVE"))
    conn.commit()
    conn.close()
    log_audit("GENERATE_LICENSE", f"Client: {client_name}, Key: {key}")
    return {"license_key": key, "client": client_name, "expires": expires, "status": "ACTIVE"}

def get_all_licenses():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM licenses")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

init_db()
