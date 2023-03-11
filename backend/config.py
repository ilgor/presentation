from os import environ

INSTANCE_NAME = 'dev-hopper-presentation'
AWS_REGION = environ.get('AWS_DEFAULT_REGION', 'us-east-2')
APP_ENVIRONMENT = environ.get('ENVIRONMENT', 'dev')
TASK_ROLE = 'dev-hopper-presentation-task'
USER_TABLE = 'dev-hopper-presentation'
APP_VERSION = '0.2.1'
S3_BUCKET = 'dev-hopper-presentation'
SLIDE_TABLE = 'dev-hopper-slides'
TRANSITION_TABLE = 'dev-hopper-transitions'
LOCAL_MEDIA_SERVER_URI = 'http://127.0.0.1:3030/'
BACKEND_SERVER_URI = 'http://127.0.0.1:5000'
