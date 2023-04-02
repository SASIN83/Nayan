from Recognize import views
from django.conf.urls import url,include
app_name = 'recognize'
urlpatterns = [
    url(r'^stream/recognize/$',views.dynamic_stream,name="videostream"),
    url(r'^stream/$',views.indexscreen, name='video'),
    url(r'^upload/$',views.indexupload, name='upload'),
    url(r'^gallary/$',views.gallary, name='gallary'),
    url(r'^image/$',views.ImageFaceDetect.as_view(), name='image'),
    url(r'^$',views.index, name='home'),
]