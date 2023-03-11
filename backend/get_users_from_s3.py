import os
import sys

branch = sys.argv[1]
file_name = 'users.csv'

def download_users():
    import boto3

    s3_client = boto3.client('s3')
    bucket = '2015ciphersecurity2020prod' if branch == 'master' else '2015ciphersecurity2020dev'
    prefix = '0admin'

    response = s3_client.list_objects(
        Bucket = bucket,
        Prefix = prefix
    )

    for file in response['Contents']:
        name = file['Key'].rsplit('/', 1)
        s3_client.download_file(bucket, file['Key'], file_name)


print('Downloading users.csv...')
download_users()


# if os.path.isfile(file_name):
#     answer = input('Found locally, do you want to override it? (y/n): ')
#     if answer.lower().strip() == 'y':
#         download_schema()
# else:
#     download_schema()