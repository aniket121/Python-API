
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Swagger Docs")

from .views import *
urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^users/', Users.as_view(), name='registerUser'),
    url(r'^login/', login.as_view(), name='loginUser'),
    url(r'^project/', project.as_view(), name='project'),
    url(r'^Images/', Images.as_view(), name='Images'),
    url(r'^search/', Search.as_view(), name='Search')
]
