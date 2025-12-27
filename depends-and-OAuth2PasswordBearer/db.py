import sqlite3

def failed(massage="gagal",data={}):
    return {
        "success":False,
        "massage":massage,
        "data":dict(data)
    }

def success(data={},massage="No massage"):
    return {
        "success":True,
        "massage":massage,
        "data":dict(data)
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
        return failed(massage="user tidak ditemukan")
    
    conn.close()
    return success(data=user)



def update_data(user_id,new_email,new_password):
    conn = foreign_key_on()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET email = ?,
                passwod = ?
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
    
    affected_row = cursor.fetchone()
    if not affected_row:
        conn.close()
        return failed(massage="User tidak di temukan")


    conn.commit()
    conn.close()
        
    return success()
