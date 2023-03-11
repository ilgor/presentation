from flask import Flask, url_for, render_template, redirect, abort, request
from flask_socketio import SocketIO
import secrets


app = Flask(__name__, static_folder='/static')
# app = Flask(__name__, static_folder='../../frontend/build/static') # For local debugging
app.config.from_pyfile('../config.py')

try:
    app.config.from_pyfile('../secrets.py')
except Exception as e:
    app.config['SECRET_KEY'] = secrets.token_urlsafe(512)
    app.secret_key = app.config['SECRET_KEY']
    app.config['SECRET_HS256'] = secrets.token_urlsafe(512)

app.debug = app.config["DEBUG"]
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'

import json
def to_pretty_json(value):
    return json.dumps(value, sort_keys=False, indent=2, separators=(',', ': '))
app.jinja_env.filters['tojson_pretty'] = to_pretty_json

# from flask_caching import Cache
# cache_config = {
#     "DEBUG": True,          # some Flask specific configs
#     "CACHE_TYPE": "simple", # Flask-Caching related configs
#     "CACHE_DEFAULT_TIMEOUT": 300
# }
# app.config.from_mapping(cache_config)
# cache = Cache(app)
socketio = SocketIO(app,
                    # async_mode="gevent",
                    engineio_logger=app.config.get('DEBUG', False),
                    socketio_logger=app.config.get('DEBUG', False),
                    # Required due to bug in socket.io , Despite single origin.
                    cors_allowed_origins=[app.config['BACKEND_SERVER_URI'],
                                          "http://localhost:5000",
                                          "http://localhost:8080",
                                          "http://localhost:80",
                                          ]
                    )
from presentation.models.form import LoginForm
from presentation.models.user import User
from presentation.utils import load_schema
from presentation.api import handler
from werkzeug.middleware.proxy_fix import ProxyFix

ProxyFix(app, x_for=1, x_host=1, x_proto=1, x_port=1)

def _set_sess(screen_number):
    user = User(user_id=screen_number)
    login_user(user)
    user.set_authenticated()

@login_manager.user_loader
def load_user(user_id):
    user = User(user_id)
    user_object = user.get_user()
    app.logger.debug(user)
    return user_object

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('schema'))
    # return render_template('index.html')

@app.route('/left', methods=['GET'])
def left():
    _set_sess('left')
    return render_template('index.html')

@app.route('/top', methods=['GET'])
def top():
    _set_sess('top')
    return render_template('index.html')

@app.route('/bottom', methods=['GET'])
def bottom():
    _set_sess('bottom')
    return render_template('index.html')

@app.route('/right', methods=['GET'])
def right():
    _set_sess('right')
    return render_template('index.html')

@app.route('/sound1', methods=['GET'])
def sound1():
    _set_sess('sound1')
    return render_template('index.html')

@app.route('/sound2', methods=['GET'])
def sound2():
    _set_sess('sound2')
    return render_template('index.html')

@app.route('/screen5', methods=['GET'])
def screen5():
    _set_sess('screen5')
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Create a blank user Object with a prospective user_id
        user = User(user_id=form.username.data)
        if user.check_password(form.password.data):
            # Set authenticated, Encode permissions from user_table into JWT and set in flask session.
            login_user(user)
            # Give them a JWT for microservices
            user.set_authenticated()
            if user.group_id == 'admin':
                return redirect(url_for('schema'))
            else:
                return redirect('/')
        else:
            abort(401)
    return render_template('login.html', title='Sign In', form=form, app_version=app.config['APP_VERSION'])


@app.route('/schema', methods=['GET', 'POST'])
def schema():
    _set_sess('admin')
    global schema
    prev_data = None

    if request.method == 'GET':
        schema = load_schema()
        emit_events(prev_data, schema.data)
        return render_template('schema.html', data=schema.data, last_page=False)

    if request.method == 'POST':
        if "nextButton" in request.form:    
            if schema.next == None:
                return render_template('schema.html', data=schema.data, last_page=True)
            prev_data = schema.data
            schema = schema.next
        elif "backButton" in request.form:
            if schema.prev == None:
                return render_template('schema.html', data=schema.data, first_page=True)
            prev_data = schema.data
            schema = schema.prev
        emit_events(prev_data, schema.data)
        return render_template('schema.html', data=schema.data, last_page=False)

def _clean(info):
    for i in range(len(info)):
        info[i] = info[i].strip()

def _adjust_url(url, media_type):
    if url.startswith("file://"):
        if "video" in media_type: 
            # url = url.replace("videos/", "") 
            url = app.config['LOCAL_MEDIA_SERVER_URI'] + "hls/" + url.replace("file://", "") + "/master.m3u8"
        elif "image" in media_type:
            url = app.config['LOCAL_MEDIA_SERVER_URI'] + url.replace("file://", "")
        elif "audio" in media_type:
            url = app.config['LOCAL_MEDIA_SERVER_URI'] + url.replace("file://", "")
        elif "thumb" in media_type:
            url = app.config['LOCAL_MEDIA_SERVER_URI'] + "thumb/" + url.replace("file://", "") + "/thumb-00.jpg"
    return url


def emit_events(prev_data, data):
    import mimetypes
    arr = []
    for key in data:
        if 'top' in key or 'left' in key or 'right' in key or 'bottom' in key or 'sound' in key or 'screen5' in key:
            url = thumb = data[key].get('urls', "") 
            loop = data[key].get('loop', False) 
            fadein = data[key].get('fadein', 0)
            fadeout = data[key].get('fadeout', 0)
            background = data[key].get('background', 'background: black')

            media_type = None

            # Local files
            if url != None and type(url) == list:
                temp_url = []
                for item in url:
                    media_type = mimetypes.MimeTypes().guess_type(item)[0]
                    temp_url.append(_adjust_url(item, media_type))
                url = temp_url
            elif url != None and url.startswith("file://"):
                media_type = mimetypes.MimeTypes().guess_type(url)[0]
                url = _adjust_url(url, media_type)

            if media_type == None:
                if "youtube" in url:
                    if "/embed/" not in url:
                        url = url.replace("watch?v=", "embed/")
                    url += "?autoplay=1"
                arr.append({'webUrl': url, 'roomId': key, 'loop': loop, 'background': background})
            elif "video" in media_type:
                if prev_data == None or data[key] != prev_data[key]:
                    arr.append({'imageUrl': url, 'roomId': key, 'loop': loop, 'background': background}) # back to back video failing. This is just a hack for now
                    arr.append({'videoUrl': url, 'roomId': key, 'loop': loop, 'background': background, 'thumb': _adjust_url(thumb, 'thumb')})
            elif "audio" in media_type:
                arr.append({'audioUrl': url, 'roomId': key, 'loop': loop, 'background': background, "fadein": fadein, "fadeout": fadeout})
            elif "image" in media_type:
                arr.append({'imageUrl': url, 'roomId': key, 'background': background, 'loop': loop})
            elif "html" in media_type:
                arr.append({'webUrl': url, 'roomId': key, 'background': background})
    for a in arr:
        socketio.emit('event', a, room=a['roomId'])
        app.logger.warning(f'Sending hooked event to: {a["roomId"]}')


if __name__ == '__main__':
    socketio.run(app)
