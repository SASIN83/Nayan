from Recognize import views
from django.urls import path, include
app_name = 'recognize'
urlpatterns = [
    path('stream/recognize/', views.dynamic_stream, name="videostream"),
    path('stream/', views.indexscreen, name='video'),
    path('upload/', views.indexupload, name='upload'),
    path('gallary/', views.gallary, name='gallary'),
    path('image/', views.ImageFaceDetect.as_view(), name='image'),
    path('', views.index, name='home'),
]