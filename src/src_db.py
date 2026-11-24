import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "cloth_image"
DB_PATH = DATA_DIR / "wardrobe.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ClothingItem (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT NOT NULL,
            color TEXT NOT NULL,
            fabric TEXT,
            season TEXT NOT NULL,
            occasion TEXT NOT NULL,
            image_path TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Outfit (
            outfit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            score REAL NOT NULL,
            item_ids TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Rating (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            outfit_id INTEGER,
            stars INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5),
            FOREIGN KEY (outfit_id) REFERENCES Outfit(outfit_id)
        )
    """)

    conn.commit()
    conn.close()


def add_clothing_item(name, item_type, color, season, occasion, fabric="", image_path=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ClothingItem (name, type, color, fabric, season, occasion, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, item_type, color, fabric, season, occasion, image_path))
    conn.commit()
    item_id = cur.lastrowid
    conn.close()
    return item_id


def get_all_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ClothingItem ORDER BY item_id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print(f"Database ready at: {DB_PATH}")