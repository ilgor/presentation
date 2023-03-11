# JWT provides a cryptographic assertion (signature) and DOES NOT provide any encryption.
import jwt
from datetime import datetime, timedelta
from flask import request, session
from flask_login import logout_user
from presentation import app


class Jwt:
    def __init__(self):
        self.id = None
        self.ttl = 3600
        self.screens_ttl = 31536000 # 1 year
        self.issuer = app.config['INSTANCE_NAME']
        self.audience = None
        self.token = request.headers.get('Authorization') or session.get('Authorization')
        self.private_key = app.config['SECRET_HS256']

    # Signs and encodes data. DOES NOT ENCRYPT.
    def encode(self, payload: dict):
        if payload.get('group_id') is 'screen':
            exp_ttl = self.expiry(self.screens_ttl)
        else:
            exp_ttl = self.expiry(self.ttl)
        jwt_payload = {
            'exp': exp_ttl,
            'nbf': datetime.utcnow(),
            'iss': app.config['INSTANCE_NAME'],
            'user_id': None,
            'group_id': None,
            'room_id': None
        }
        jwt_payload.update(payload)
        enc_jwt = jwt.encode(jwt_payload, self.private_key, algorithm='HS256')
        return enc_jwt

    # Verified signature of payload data.
    def decode(self):
        ret = dict()
        if self.token is None:
            ret['success'] = False
            return ret
        try:
            ret['jwt'] = jwt.decode(self.token, self.private_key, algorithms=['HS256'])
            ret['success'] = True
            return ret
        except jwt.ExpiredSignatureError as e:
            app.logger.critical(f'Expired Signature: {e}')
            session = None
            ret['success'] = False
            return ret

    def expiry(self, ttl):
        now = datetime.utcnow().replace(tzinfo=None)
        expiry = now + timedelta(seconds=ttl)

        return expiry
