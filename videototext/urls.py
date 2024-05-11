from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from videototext.api.apiviews import KeywordsApiView, ArchivoApiView, TransciptionApiView
from .views import upload_file

# Creando esquema de configuracion para la auto doc de swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Transcription API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Creando el router
router = routers.DefaultRouter()

# Keywords endpoints
router.register(r'keywords', KeywordsApiView)
# Archivos endpoints
router.register(r'files', ArchivoApiView)

urlpatterns = [
    path('', upload_file, name="home-app"),
    path('demo', upload_file, name="demo-app"),
    # Web API
    path('api/v1/transcription-app', TransciptionApiView.as_view(), name='transcription-app'),
    path('api/v1/', include(router.urls)),
    # auto documentation config
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
