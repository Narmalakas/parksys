from database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def register_user(self, user_type, first_name, last_name, email, phone, password):
        query = """
            INSERT INTO Users (UserType, FirstName, LastName, Email, PhoneNumber, Password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.db.execute(query, (user_type, first_name, last_name, email, phone, password))
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def authenticate_user(self, email, password):
        query = "SELECT * FROM Users WHERE Email=%s AND Password=%s"
        return self.db.fetch_one(query, (email, password))
