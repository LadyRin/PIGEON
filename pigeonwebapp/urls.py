from rest_framework.routers import DefaultRouter
from pigeonwebapp.views import EventViewSet, EventTypeViewSet, EventThemeViewSet, MailingListViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event_types', EventTypeViewSet)
router.register(r'event_themes', EventThemeViewSet)
router.register(r'mailing_lists', MailingListViewSet)

urlpatterns = router.urls
