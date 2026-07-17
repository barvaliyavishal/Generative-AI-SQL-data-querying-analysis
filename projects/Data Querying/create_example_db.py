import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "example.db"


def create_example_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            join_date TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product TEXT,
            amount REAL,
            sale_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
        )
        """
    )

    customers = [
        (1, "Asha Sharma", "asha@example.com", "2023-01-15"),
        (2, "Rahul Verma", "rahul@example.com", "2022-11-03"),
        (3, "Priya Singh", "priya@example.com", "2023-03-22"),
    ]
    sales = [
        (1, 1, "Laptop", 1200.0, "2023-03-05"),
        (2, 2, "Monitor", 300.0, "2023-03-12"),
        (3, 1, "Mouse", 25.0, "2023-03-15"),
        (4, 3, "Keyboard", 45.0, "2023-04-02"),
        (5, 2, "Laptop", 1100.0, "2023-05-20"),
    ]

    cursor.executemany("INSERT OR IGNORE INTO customer VALUES (?,?,?,?)", customers)
    cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)", sales)

    conn.commit()
    conn.close()
    print(f"{DB_PATH.name} created/updated with sample data.")


if __name__ == "__main__":
    create_example_db()
