from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
import jwt
from django.core.files.storage import FileSystemStorage 
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator
from mattersmithapp.models import *
from functools import wraps
import os
from rest_framework_jwt.settings import api_settings
import base64
from mattersmithapp.serializers import *
from django.db.models import Q
from django.core.paginator import Paginator
from mattersmithapp.document import userTrack
import logging
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.
class Case(APIView):
	 def get(paginatedData,pageNumbers):
	 	 return Response({'msg':"this is Subapp"})
