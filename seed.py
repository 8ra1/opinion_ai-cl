import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "database/opinion_ai.db"

CATEGORIES = [
    "Food Quality",
    "Cleanliness",
    "Staff Behavior",
    "Price"
]

USERS = [
    {
        "email": "owner@opinion.ai",
        "password": "owner123",
        "user_type": "owner"
    },
    {
        "email": "admin@opinion.ai",
        "password": "admin123",
        "user_type": "admin"
    }
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for category in CATEGORIES:
    cursor.execute(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)",
        (category,)
    )

for user in USERS:
    password_hash = generate_password_hash(user["password"])

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (email, password_hash, user_type)
        VALUES (?, ?, ?)
        """,
        (user["email"], password_hash, user["user_type"])
    )

conn.commit()
conn.close()

print("Seed data inserted successfully.")