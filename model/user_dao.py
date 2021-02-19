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

    def get_followed(self, user_id, follow_id):
        return self.db.execute(text("""
            SELECT IF (EXISTS (
                SELECT * FROM users_follow_list
                WHERE user_id=:id AND follow_user_id=:follow
            ),1,0)
        """),{'id':user_id, 'follow':follow_id}).fetchone()

    def insert_follow(self, user_id, follow_id):
        return self.db.execute(text("""
            INSERT INTO users_follow_list(
                user_id,
                follow_user_id
            ) VALUES (
                :id,
                :follow
            )
        """), {'id':user_id, 'follow':follow_id}).rowcount

    def update_follow(self, user_id, follow_id, status):
        return self.db.execute(text("""
            UPDATE users_follow_list
            SET followed=:status
            WHERE user_id=:id AND follow_user_id=:follow
        """), {'id':user_id, 'follow':follow_id, 'status':status}).rowcount
    