from sqlalchemy import text

class UserDao:
    def __init__(self, database):
        self.db=database

    def get_user(self, user_id):
        user=self.db.execute(text("""
            SELECT
                id,
                name,
                profile
            FROM users
            WHERE id=:user_id
        """),{'user_id':user_id}).fetchone()

        return {
            'id':user['id'],
            'name':user['name'],
            'profile':user['profile'],
        } if user else None

    def insert_user(self, user):
        return self.db.execute(text("""
            INSERT INTO users (
                name,
                email,
                hashed_password,
                profile
            ) VALUES (
                :name,
                :email,
                :password,
                :profile
            )
        """),user).lastrowid

    def get_user_id_and_password(self, email):
        row=self.db.execute(text("""
            SELECT
                id,
                hashed_password
            FROM users
            WHERE email=:email
        """),{'email':email}).fetchone()
        
        return row if row else None