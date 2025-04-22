# copercore-ai/urls.py

from django.urls import path
from . import  views 

urlpatterns = [
    path('upload/', views.upload_view, name='upload'),
    path('dataset/upload/', views.upload_dataset, name='upload_dataset'),
    path('project/', views.project_view, name='project'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/dataset/upload/', views.dataset_upload, name='dataset_upload'),
    path('map/', views.map_view, name='map'),
    path('help/', views.help_view, name='help'),
]