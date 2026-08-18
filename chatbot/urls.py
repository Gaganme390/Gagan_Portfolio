from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat, name='chat'),
    path('refresh/', views.refresh_index, name='refresh_index'),
]
