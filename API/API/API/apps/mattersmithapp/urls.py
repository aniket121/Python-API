
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from .views import *
schema_view = get_swagger_view(title="Swagger Docs")


urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^users/', Users.as_view(), name='registerUser'),
    #url(r'^login/', login.as_view(), name='loginUser'),
    url(r'^project/', project.as_view(), name='project'),
    #url(r'^images/(?P<user_id>[ \w-]+)/(?P<device_token>[ \w-]+)/$', Images.as_view(), name='Images'),
    url(r'^images/', Images.as_view(), name='Images'),
    url(r'^search/$', Search.as_view(), name='Search'),
    #url(r'^case/', include('mattersmithapp.case.urls',namespace='case'))
]
