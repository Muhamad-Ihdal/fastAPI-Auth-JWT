import sqlite3

def delete_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")

    conn.commit()
    conn.close()
    return

def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id  INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT NOT NULL
    )"""
    )

    conn.commit()
    conn.close()
    return



def add_user(email,password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email,password) VALUES (?,?);",
            (email,password)
        )
    except sqlite3.IntegrityError:
        conn.commit()
        conn.close()
        return "Email telah digunakan"


    conn.commit()
    conn.close()
    return "User berhasil ditambahkan"

def user_account(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()


    cursor.execute(
        "SELECT password FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    return user[0]


