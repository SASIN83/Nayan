from Recognize import views
from django.conf.urls import url,include
app_name = 'recognize'
urlpatterns = [
    url(r'^stream/recognize/$',views.dynamic_stream,name="videostream"),
    url(r'^stream/$',views.indexscreen, name='video'),
    url(r'^$',views.index),
]