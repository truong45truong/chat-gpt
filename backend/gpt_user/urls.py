"""
URL configuration for backend project.

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
from django.urls import path, include

urlpatterns = [
    path('', include('gpt_base.urls')),
    path('api/members/', include('gpt_user.members.urls')),
    path('api/prompts/', include('gpt_user.prompts.urls')),
    path('api/chat-gpt/', include('gpt_user.chat_gpt.urls')),
    path('api/conversations/', include('gpt_user.conversations.urls')),
    path('api/grammarly/', include('gpt_user.grammarly.urls')),
    path('api/documents/', include('gpt_user.documents.urls')),
]
