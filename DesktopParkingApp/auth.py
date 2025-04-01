import mysql.connector
from database import connect_db
from bcrypt import checkpw

def authenticate_user(email, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and checkpw(password.encode('utf-8'), user["Password"].encode('utf-8')):
            return user  # Return user details if authentication is successful
    return None
