from rest_framework import viewsets
import paramiko
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from pigeonwebapp.tasks import update_servers_with_json

class SSHViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'])
    def generate_key_pair(self, request):
        open("private_key", "w").close()

        # Generate RSA key pair
        key = paramiko.RSAKey.generate(2048)

        key.write_private_key_file("private_key")
        public_key = key.get_name() + " " + key.get_base64()
        return Response({"public_key": public_key})
    
    @action(detail=False, methods=['get'])
    def public_key(self, request):
        # Get public key
        try:
            key = paramiko.RSAKey.from_private_key_file("private_key")
        except IOError:
            return Response({"public_key": "Not yet generated"})
        public_key = key.get_name() + " " + key.get_base64()
        return Response({"public_key": public_key})
    
    @action(detail=False, methods=['post'])
    def update_servers(self, request):
        update_servers_with_json.delay(force=True)
        return Response({"message": "Servers update started"})