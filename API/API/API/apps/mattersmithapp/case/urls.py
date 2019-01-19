
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from .views import *
schema_view = get_swagger_view(title="Swagger Docs")


urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^case/', Case.as_view(), name='case'),
    
]
