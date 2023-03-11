import os
import sys

branch = sys.argv[1]
is_default = len(sys.argv) > 2 and sys.argv[2] == 'default'

def create_folders():
    folders = ['sounds', 'videos', 'images']
    for folder in folders:
        path = f'../media/{folder}'
        if not os.path.isdir(path):
            os.mkdir(path)


def push_schema():
    import boto3

    s3_client = boto3.client('s3')
    bucket = '2015ciphersecurity2020prod' if branch == 'master' else '2015ciphersecurity2020dev'
    prefix = 'default_schema' if is_default else 'schema'
    file_name = 'schema.json'

    response = s3_client.response = s3_client.upload_file(file_name, bucket, f'{prefix}/{file_name}')

push_schema()