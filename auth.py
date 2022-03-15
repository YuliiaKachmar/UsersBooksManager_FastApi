import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
import datetime


class Auth():
    hasher = CryptContext(schemes=['bcrypt'])
    secret = "APP_SECRET_STRING"

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, user):
        vdate = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({"user_id": user.id, "is_admin": user.is_admin, 'exp': vdate}, self.secret)

        return {"access_token": token,
                "token_type": "bearer"}

    def decode_token(self, token):
        try:
            decoded_token = jwt.decode(token, self.secret, algorithm='HS256')
            if decoded_token["expires"] >= datetime.datetime.utcnow():
                return decoded_token
            else:
                raise jwt.ExpiredSignatureError
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

