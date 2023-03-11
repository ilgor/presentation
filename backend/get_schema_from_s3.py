import os
import sys

branch = sys.argv[1]
is_default = len(sys.argv) > 2 and sys.argv[2] == 'default'

def download_schema():
    import boto3

    s3_client = boto3.client('s3')
    bucket = '2015ciphersecurity2020prod' if branch == 'master' else '2015ciphersecurity2020dev'
    prefix = 'default_schema' if is_default and branch == 'dev' else 'schema'

    response = s3_client.list_objects(
        Bucket = bucket,
        Prefix = prefix
    )

    for file in response['Contents']:
        name = file['Key'].rsplit('/', 1)
        s3_client.download_file(bucket, file['Key'], file_name)


file_name = 'schema.json'

if os.path.isfile(file_name):
    answer = input('Found schema.json locally, do you want to override it? (y/n): ')
    if answer.lower().strip() == 'y':
        print('Downloading schema.json...')
        download_schema()
        print('Done!')
    else:
        print('Skipped!')
else:
    print('Downloading schema.json...')
    download_schema()
    print('Done!')