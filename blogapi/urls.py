from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(title="BlogPosts API", default_version='v1',
                 description="A proxy API to external CodeLeap careers endpoint"),
    public=True,
    permission_classes=(permissions.AllowAny,),
   # schemes=['http', 'https']
    url= "https://127.0.0.1:3333" if not settings.DEBUG else "http://127.0.0.1:3333",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]