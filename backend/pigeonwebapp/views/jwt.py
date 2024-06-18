from rest_framework_simplejwt.views import TokenObtainPairView

from pigeonwebapp.serializers.jwt import CustomObtainPairSerializer


# https://stackoverflow.com/questions/36938404/adding-information-to-jwt-token-body-using-django-rest-framework-jwt

class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer
