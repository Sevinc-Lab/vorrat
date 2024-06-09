import sqlite3
from datetime import datetime, timedelta

def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_expiry_date(purchase_date, shelf_life):
    if shelf_life is None:
        return None
    purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
    return (purchase_date + timedelta(days=shelf_life)).strftime('%Y-%m-%d')
