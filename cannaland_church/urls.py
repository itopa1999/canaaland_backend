from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Canaanland API",
        default_version="v1",
        description="API description for Canaanland App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('admins/api/', include('administrator.urls')),
    path('users/api/', include('users.urls')),
    path('logec/api/', include('logec.urls')),
    path('gmghf/api/', include('gmghf.urls')),
    path('nysc_church/api/', include('nysc_church.urls')),
    
    path(
        "doc/",
        include(
            [
                path(
                    "swagger/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
                path(
                    "swagger.json",
                    schema_view.without_ui(cache_timeout=0),
                    name="schema-json",
                ),
                path(
                    "redoc/",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),
            ]
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)