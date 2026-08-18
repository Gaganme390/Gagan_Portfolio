from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('download-resume/', views.download_resume, name='download_resume'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
]
