from rest_framework.routers import DefaultRouter
from pigeonwebapp.views import EventViewSet, EventTypeViewSet, EventThemeViewSet, MailingListViewSet, CustomObtainPairView
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Pigeon API",
        default_version='v1',
        description="Pigeon API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aaa"),
        license=openapi.License(name="GNU Public License"),
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event_types', EventTypeViewSet)
router.register(r'event_themes', EventThemeViewSet)
router.register(r'mailing_lists', MailingListViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('token', CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    # Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]