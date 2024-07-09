from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action

from pigeonwebapp.services.booking import Booker

class BookingViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def resources(self, request):
        try:
            booker = Booker()
            booker.authenticate()
            resources = booker.get_all_resources()
            return Response(resources)
        except Exception as e:
            return Response({
                "resources": [],
            })