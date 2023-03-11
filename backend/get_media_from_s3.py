import os
import sys

answer = input('Do you want to sync media? (y/n): ')
if answer.lower().strip() == 'y':
    branch = sys.argv[1]
    bucket = '2015ciphersecurity2020prod' if branch == 'master' else '2015ciphersecurity2020dev'
    cmd = f'aws s3 sync s3://{bucket}/ ./media/'
    os.system(cmd)