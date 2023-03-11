import os
import sys
from colors import *
import socket
import webbrowser


orig_config = "config.py"
updated_config = "updated_config.py"
has_changed = False

hostname = socket.gethostname()    
ip_address = socket.gethostbyname(hostname)

with open(orig_config) as fin, open(updated_config, 'w') as fout:
    for line in fin:
        lineout = line
        if 'LOCAL_MEDIA_SERVER_URI' in line.strip():
            lineout = f"LOCAL_MEDIA_SERVER_URI = 'http://{ip_address}:3030/'\n"
            has_changed = True
        elif 'BACKEND_SERVER_URI' in line.strip():
            lineout = f"BACKEND_SERVER_URI = 'http://{ip_address}:5000'\n"
            has_changed = True
        fout.write(lineout)
if has_changed:
    os.rename(updated_config, orig_config)


sys.stdout.writelines(BCyan + UCyan)
print(f'\n\nYour local media is running on: http://{ip_address}:3030/\n')
print(f'Test video on Safari: http://{ip_address}:3030/hls/bad-day.mp4/master.m3u8\n')
print(f'Test image on Safari: http://{ip_address}:3030/images/aws.png\n')
sys.stdout.write(Color_Off)
webbrowser.open(f'http://{ip_address}:5000/schema', new = 2)