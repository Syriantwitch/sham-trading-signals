import sqlite3
import uuid
from datetime import datetime
from backend.app.db.database import DB_PATH

class PaymentService:
    @staticmethod
    def submit_payment(user_id: str, email: str, plan: str, amount: float, tx_id: str, sender: str):
        payment_id = str(uuid.uuid4())[:8].upper()
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        status = "PENDING_VERIFICATION"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (payment_id, user_id, email, plan, amount, transaction_id, sender_account, status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (payment_id, user_id, email, plan, amount, tx_id, sender, status, timestamp))
        conn.commit()
        conn.close()

        return {
            "payment_id": payment_id,
            "user_id": user_id,
            "email": email,
            "plan": plan,
            "amount": amount,
            "transaction_id": tx_id,
            "sender_account": sender,
            "status": status,
            "timestamp": timestamp
        }

    @staticmethod
    def get_all_payments():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments ORDER BY timestamp DESC")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def update_payment_status(payment_id: str, new_status: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE payments SET status = ? WHERE payment_id = ?", (new_status, payment_id))
        conn.commit()
        conn.close()
        return {"payment_id": payment_id, "new_status": new_status}
