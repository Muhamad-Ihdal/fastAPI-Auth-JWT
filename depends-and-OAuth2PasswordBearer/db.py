import sqlite3


def foreign_key_on():
    conn = sqlite3.connect("users.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = foreign_key_on()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXITS users(
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()
    return




def add_user(email,hashed_password):
    conn = foreign_key_on()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO (email,password) VALUES (?,?)",
            (email,hashed_password)
        )
    except sqlite3.IntegrityError:
        conn.close()
        return None
        
    user = get_user_by_email(email=email)

    conn.commit()
    conn.close()
    return user




def get_user_by_id(user_id:int):
    conn = foreign_key_on()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    if not user:
        conn.close()
        return None
    
    conn.close()
    return user


def get_user_by_email(email:str):
    conn = foreign_key_on()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    if not user:
        conn.close()
        return None
    
    conn.close()
    return user