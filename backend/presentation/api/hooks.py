from presentation import app, socketio
from flask_login import login_required
from flask import request
from presentation.utils import slide_scan
import json


@app.route('/hooks', methods=['PUT', 'POST'])
@login_required
def hooks():
    app.logger.info(f'Received hook:\n{str(request)}')
    try:
        transition = list()
        for slide in slide_scan(request.json['transitionId']):
            if app.config['LOCAL_MEDIA_SERVER_URI']:
                if slide.get('imageUrl'):
                    imageUrl = f"{app.config['LOCAL_MEDIA_SERVER_URI']}/{str.join('/', slide['imageUrl'].split('?')[0].split('/')[3::])}"
                    videoUrl = None
                if slide.get('videoUrl'):
                    videoUrl = f"{app.config['LOCAL_MEDIA_SERVER_URI']}/{str.join('/', slide['videoUrl'].split('?')[0].split('/')[3::])}"
                    imageUrl = None
                hook = {
                    'imageUrl': imageUrl,
                    'videoUrl': videoUrl,
                    'slideId': slide['slideId'],
                    'transitionId': slide['transitionId'],
                    'roomId': slide['roomId']
                }
            else:
                hook = {
                    'imageUrl': slide['imageUrl'],
                    'videoUrl': slide['videoUrl'],
                    'slideId': slide['slideId'],
                    'transitionId': slide['transitionId'],
                    'roomId': slide['roomId']
                }
            transition.append(hook)
        for hook in transition:
            app.logger.warning(f'Sending hooked event to: {hook["roomId"]}')
            socketio.emit('event', hook, room=hook['roomId'])
        return 'Hooks Succeeded', 200
    except Exception as e:
        app.logger.critical(f'Invalid hook!: {e}')
        return 'Hook Failed', 400


# Legacy route for step function/SQS based hooks
# @app.route('/sfn_hook', methods=['POST'])
# @login_required
# def sfn_hook():
#     app.logger.info(f'Received hook:\n{str(request.json)}')
#     try:
#         hook = json.loads(request.json['Message'])
#         app.logger.debug(f'Received hook: {hook}')
#         socketio.emit('event', json.dumps(hook), room=hook['room_id'])
#         return 'Hook succeeeded', 200
#     except Exception as e:
#         app.logger.critical(f'Invalid hook!: {e}')
#         return 'Failed to hook\n', 418
