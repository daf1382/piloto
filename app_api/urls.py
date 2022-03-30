from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('helloworld/', views.hello_world),
    path('upload/', views.upload_file),
    path('month/', views.month),    
]




 #   path('', views.IndexView.as_view(), name='index'),
