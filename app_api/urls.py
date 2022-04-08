from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('upload/', views.upload_file),
    path('pasos/', views.pasos),    
]





