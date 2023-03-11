from flask import session, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import user_needs_refresh
from presentation import app
from presentation.models.jwt import Jwt
from presentation.models.ddb import Ddb


class User:
    def __init__(self, user_id: str, room_id: str = None, group_id: str = None):
        # self.user_id = session.get('user_id', user_id)
        self.user_id = user_id
        self.group_id = group_id
        self.room_id = room_id
        self.user_token = Jwt()
        self.default_ttl = 3600*100

    def __repr__(self):
        return {'user_id': self.user_id,
                'group_id': self.group_id,
                'room_id': self.room_id}

    def __str__(self):
        return str({'user_id': self.user_id,
                    'group_id': self.group_id,
                    'room_id': self.room_id})

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        pass

    def check_password(self, password):
        app.logger.debug(f'Checking user password for {self.user_id}')
        ddb = Ddb()
        stored_password = ddb.get_user_password(self.user_id)
        # return check_password_hash(stored_password, password)
        return stored_password == password

    def get_user(self):
        if self.user_token.token:
            app.logger.debug('Using JWT for User model')
            self.refresh_user()
            return self
        else:
            app.logger.debug('Using DDB for User model')
            ddb = Ddb()
            get_user = ddb.get_user(self.user_id)
            self.user_id = self.user_id
            self.room_id = get_user[0]
            self.group_id = get_user[2]
            self.room_id = get_user[3]

    def refresh_user(self):
        user_data = self.validate_jwt()
        if user_data.get('user_id'):
            self.user_id = user_data[0]
            self.group_id = user_data[2]
            self.room_id = user_data[3]
            return True
        else:
            ddb = Ddb()
            get_user = ddb.get_user(self.user_id)
            self.user_id = self.user_id
            self.group_id = get_user[2]
            self.room_id = get_user[3]
            return False

    def validate_jwt(self):
        res = self.user_token.decode()
        if res['success']:
            return res
        else:
            return res

    def is_authenticated(self):
        app.logger.debug(f'Checking is_authenticated for {self.user_id}')
        if self.user_token.token:
            authenticated = self.validate_jwt()
            if authenticated.get('user_id'):
                self.user_id = authenticated['user_id']
                self.group_id = authenticated['group_id']
                self.room_id = authenticated['room_id']
                app.logger.debug('Authenticated: {0}'.format(authenticated))
                return True
            else:
                app.logger.critical(
                    'User token failed authentication: {0}'.format(self.user_id))
                return False
        else:
            app.logger.warning('User token is None')
            return False

    def set_authenticated(self):
        self.get_user()
        app.logger.info(f'Setting {self.user_id} authenticated')
        session['user_id'] = self.user_id
        payload = {
            'user_id': self.user_id,
            'group_id': self.group_id,
            'room_id': self.room_id,
        }
        try:
            session['Authorization'] = self.user_token.encode(payload)
        except Exception as e:
            app.logger.critical(
                f'Failed to encode user_id token: {self.user_id}')
            return abort(400)

    def get_id(self):
        return self.user_id

    # Used for signups.
    def put_user(self):
        pass

    def is_active(self):
        pass

    def is_anonymous(self):
        pass
