from pigeonwebapp.models import Server
import paramiko
from django.conf import settings
import paramiko.hostkeys
import paramiko.util
import os


def upload_file(server: Server, file: str):
    private_key = paramiko.RSAKey.from_private_key_file('private_key')
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server.hostname, username=server.username, pkey=private_key, port=server.port, banner_timeout=200, timeout=200)
    sftp = client.open_sftp()

    sftp.put(file, os.path.join('/', server.upload_directory, file))

    sftp.close()
    client.close()
