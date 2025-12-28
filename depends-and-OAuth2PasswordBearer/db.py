import sqlite3

def failed(massage="gagal",data=None):
    if data :
        data = dict(data)
    return {
        "success":False,
        "massage":massage,
        "data":data
    }

def success(massage="No massage",data=None):
    if data :
        data = dict(data)
    return {
        "success":True,
        "massage":massage,
        "data":data
    }

def foreign_key_on():
    conn = sqlite3.connect("users.db")
    # conn = sqlite3.connect("depends-and-OAuth2PasswordBearer/users.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = foreign_key_on()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()
    return

def create_table_refresh_token():
    conn = foreign_key_on()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refresh_token(
        id INTEGER PRIMARY KEY,
        expired_at TEXT NOT NULL,
        token TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    )""")

    conn.commit()
    conn.close()
    return

def add_refresh_token(expired,user_id:int,token:str):
    conn = foreign_key_on()
    cursor = conn.cursor()


    cursor.execute(
        "INSERT INTO refresh_table (expired_at,user_id,token) VALUES (?,?,?)",
        (expired,user_id,token)
    )
    affected_row = cursor.rowcount
    if not affected_row:
        return failed()

    conn.commit()
    conn.close()
    return success()

def is_exists_refresh_token(token:str):
    conn = foreign_key_on()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM refresh_token WHERE token = ?",
        (token,)
    )

    row = cursor.fetchone()
    if not row:
        conn.close()
        return failed(massage="gada")

    conn.close()
    return success(data=row)

def delete_token(token:str):
    conn = foreign_key_on()
    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM refresh_token WHERE token = ?",
        (token,)
    )

    conn.commit()
    conn.close()
    return




def add_user(email,hashed_password):
    conn = foreign_key_on()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email,password) VALUES (?,?)",
            (email,hashed_password)
        )
    except sqlite3.IntegrityError:
        conn.close()
        return failed(massage="Email telah digunakan")
    conn.commit()
    conn.close()
        
    user = get_user_by_email(email=email)

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
        return failed(massage="user tidak ditemukan")
    
    conn.close()
    return success(data=user)


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
        return failed(massage="user tidak ditemukan ")
    
    conn.close()
    return success(data=user)


def update_data(user_id,new_email,new_password):
    conn = foreign_key_on()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET email = ?,
                password = ?
            WHERE id = ?""",
            (new_email,new_password,user_id))

    except sqlite3.IntegrityError:
        conn.close()
        return failed(massage="Email telah digunakan")

    conn.commit()
    conn.close()
        
    user = get_user_by_email(email=new_email)
    return user

def delete_data(user_id):
    conn = foreign_key_on()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,))
    
    affected_row = cursor.rowcount
    if not affected_row:
        conn.close()
        return failed(massage="User tidak ditemukan ")

    conn.commit()
    conn.close()
        
    return success()
