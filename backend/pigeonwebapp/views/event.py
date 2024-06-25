from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator

from pigeonwebapp.models.event import Event
from pigeonwebapp.serializers.event import EventReadSerializer, EventWriteSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventReadSerializer
    queryset = Event.objects.all().order_by('-date', '-start_time')
    permission_classes = [IsAuthenticated]

    def list(self, request):
        query_search = request.query_params.get('search', None)
        current_page = request.query_params.get('current_page', 1)

        if query_search:
            events = Event.objects.filter(title__icontains=query_search).order_by('-date', '-start_time')
        else:
            events = Event.objects.all().order_by('-date', '-start_time')

        per_page = request.query_params.get('per_page', len(events))
        p = Paginator(events, per_page)

        if int(current_page) > p.num_pages:
            current_page = p.num_pages

        serializer = EventReadSerializer(instance=p.page(current_page).object_list, many=True)

        return Response({
            'count': p.count,
            'num_pages': p.num_pages,
            'start_index': p.page(current_page).start_index(),
            'end_index': p.page(current_page).end_index(),
            'results': serializer.data
        },
            status=status.HTTP_200_OK)


    def create(self, request):
        user = request.user
        serializer = EventWriteSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
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