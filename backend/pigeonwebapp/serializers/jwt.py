from datetime import date
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from pigeonwebapp.tasks import add

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        add.delay(2, 3)
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['username'] = self.user.username
        data['date'] = str(date.today())
        data['is_admin'] = self.user.is_superuser
        return data