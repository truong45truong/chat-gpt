"""
URL configuration for gpt_base project.

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
from django.shortcuts import redirect
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from gpt_base import settings

swagger_view = []
if settings.DISPLAY_SWAGGER:
    swagger_view = [
        path('', lambda request: redirect('api/', permanent=True)),
        path(
            'api/',
            SpectacularSwaggerView.as_view(
                template_name='swagger-ui.html',
                url_name="schema"
            ),
            name="swagger-ui",
        ),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='re-doc'),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    ]

urlpatterns = swagger_view + [
    path('admin/', admin.site.urls),
    path('api/auth/', include('gpt_base.auth.urls')),
]
