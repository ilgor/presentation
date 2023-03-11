from presentation import app, socketio
from flask_socketio import send, join_room
from flask import request, redirect, url_for, session
from flask_login import current_user
from presentation.utils import authenticated_only


@socketio.on('connect')
@authenticated_only
def connect():
    if current_user.is_authenticated:
        if current_user.group_id is 'screen':
            app.logger.debug('A screen connected!')
            pass
        # Joining configured room_id to receive websocket hooks
        join_room(current_user.room_id)
        log_msg = f"Flask Websocket connected, room_id: {current_user.room_id}, {str(request.remote_addr)}"
        app.logger.debug(log_msg)
        send(log_msg)
    else:
        app.logger.critical('Current user is not authenticated, Refusing websocket')
        redirect(url_for('login'))


@socketio.on('message')
@authenticated_only
def handle_message(message):
    app.logger.warning(f'{session.id} client message: ' + message)
    send('This is Flask, You messaged me just now. Would you like some JSON? I have lots of JSON!')
    send(message)


@socketio.on('event')
@authenticated_only
def handle_event(event):
    app.logger.debug('event: ' + event['Message'])


@socketio.on('disconnect')
@authenticated_only
def disconnect():
    app.logger.warning('Client disconnected')


@socketio.on_error()
def error_handler(e):
    app.logger.critical(f'A Socket IO error occurred!: {e}')


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    app.logger.error(e)
