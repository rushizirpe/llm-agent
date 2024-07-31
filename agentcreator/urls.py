"""agentcreator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from agentcreator import views


urlpatterns = [
    path('', views.index, name='index'),
    path('launch/', views.launch_api, name='launch_api'),
    path('stop/', views.stop_api, name='stop_api'),
    path('v1/chat/completions/', views.chat_completion, name='chat_completion'),
    path('v1/embeddings/', views.get_embeddings, name='get_embeddings'),
    path('api/', views.api_view, name='api_view'),
]