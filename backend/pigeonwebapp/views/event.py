from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from pigeonwebapp.models.event import Event
from pigeonwebapp.serializers.event import EventReadSerializer, EventWriteSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventReadSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            user = request.user
            serializer = EventWriteSerializer(data=request.data, context={'user': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        event = self.get_object()

        if user != event.owner and not user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = EventWriteSerializer(event, data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        user = request.user
        event = self.get_object()

        if user != event.owner and not user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)