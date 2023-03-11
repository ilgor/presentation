import os
import socket


orig_hosts = "/etc/hosts"
updated_hosts = "/etc/updated_hosts"

custom_url = "mb.c"

def update_hosts():
    hostname = socket.gethostname()    
    ip_address = socket.gethostbyname(hostname) 
    custom_host_exists = False
    with open(orig_hosts) as fin, open(updated_hosts, 'w') as fout:
        for line in fin:
            lineout = line
            print(lineout)
            if custom_url in line.strip():
                lineout = f"{ip_address}    {custom_url}\n"
                custom_host_exists = True
            fout.write(lineout)
        if not custom_host_exists:
            lineout = f"{ip_address}    {custom_url}\n"
            fout.write(lineout)
    os.rename(updated_hosts, orig_hosts)

update_hosts()