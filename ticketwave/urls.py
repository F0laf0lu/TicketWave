"""
URL configuration for ticketwave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view as swagger_view
from drf_yasg import openapi


schema_view = get_schema_view(
    title='Ticketwave API',
    public=True, 
    permission_classes=(AllowAny,))


schema_view2 = swagger_view(
    openapi.Info(
        title="Ticketwave API",
        default_version="v1",
        description="API documentation of Smart Learning", 
        license=openapi.License(name="BSD License"),
        ),
    public=True,
    permission_classes=[AllowAny],)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('users/', include('users.urls')),
    path('schema/', schema_view), 
    path('docs/', include_docs_urls(title='Tickewave API')),
    path("__debug__/", include("debug_toolbar.urls")),

    path('', schema_view2.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view2.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
