from rest_framework.routers import DefaultRouter
from pigeonwebapp.views import EventViewSet, EventTypeViewSet, EventThemeViewSet, MailingListViewSet
from pigeonwebapp.views.login import LDAPLogin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event_types', EventTypeViewSet)
router.register(r'event_themes', EventThemeViewSet)
router.register(r'mailing_lists', MailingListViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LDAPLogin.as_view(), name='ldap_login')
]