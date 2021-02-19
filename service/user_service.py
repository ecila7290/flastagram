import jwt
import bcrypt

from datetime import datetime, timedelta

class UserService:
    def __init__(self, user_dao, config):
        self.user_dao=user_dao
        self.config=config

    def get_user(self, user_id):
        user=self.user_dao.get_user(user_id)

        return user

    def create_new_user(self, new_user):
        new_user['password']=bcrypt.hashpw(new_user['password'].encode('utf-8'),bcrypt.gensalt())
        new_user_id=self.user_dao.insert_user(new_user)

        return new_user_id

    def get_user_id_and_password(self, email):
        user_credential=self.user_dao.get_user_id_and_password(email)
        
        return user_credential

    def login(self,credential):
        email=credential['email']
        password=credential['password']
        user_credential=self.user_dao.get_user_id_and_password(email)

        authorized=user_credential and bcrypt.checkpw(password.encode('utf-8'), user_credential['hashed_password'].encode('utf-8'))

        return authorized

    def generate_access_token(self, user_id):
        payload={'user_id':user_id, 'exp':datetime.utcnow()+timedelta(seconds=60*60*24)}
        token=jwt.encode(payload, self.config['JWT_SECRET_KEY'], self.config['ALGORITHM'])

        return token

    def follow(self, user_id, follow_id):
        followed=self.user_dao.get_followed(user_id, follow_id)
        
        if followed[0]:
            return self.user_dao.update_follow(user_id, follow_id, 1)
        else:
            return self.user_dao.insert_follow(user_id, follow_id)

    def unfollow(self, user_id, follow_id):
        return self.user_dao.update_follow(user_id, follow_id, 0)