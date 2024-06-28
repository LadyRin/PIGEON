from pigeonwebapp.models import Server
import paramiko
from django.conf import settings
import paramiko.hostkeys
import paramiko.util
import os

def ssh_connection(server: Server):
    # SSH connection
    transport = paramiko.Transport((server.hostname, server.port))    

    private_key = paramiko.RSAKey.from_private_key_file('private_key')

    transport.connect(username=server.username, pkey=private_key)

    return transport

def upload_file(server: Server, file: str):
    with ssh_connection(server) as t:
        sftp = paramiko.SFTPClient.from_transport(t)

        remote_file = os.path.join('/', server.upload_directory, os.path.basename(file))

        print(f"Uploading {file} to {remote_file}")

        if sftp:
            sftp.put(file, remote_file)
        t.close()