import sqlite3
import hashlib
from backend.app.db.database import DB_PATH

class AffiliateService:
    @staticmethod
    def generate_code(email: str) -> dict:
        clean_email = email.strip().lower()
        code = "SHAM-" + hashlib.md5(clean_email.encode()).hexdigest()[:6].upper()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO affiliates (code, owner_email, referrals_count, bonus_days)
            VALUES (?, ?, 0, 0)
        ''', (code, clean_email))
        conn.commit()
        cursor.execute("SELECT code, owner_email, referrals_count, bonus_days FROM affiliates WHERE code = ?", (code,))
        row = cursor.fetchone()
        conn.close()
        return {
            "referral_code": row[0],
            "owner": row[1],
            "referrals_count": row[2],
            "bonus_days": row[3],
            "invite_link": f"https://t.me/ShamSignalsBot?start={row[0]}"
        }
