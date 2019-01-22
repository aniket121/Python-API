# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
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
import json
# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.

class Login(APIView):
	  permission_classes = (permissions.AllowAny,)

	  def post(self, request):
	  	  try:
	  	 	body_unicode = request.body.decode("utf-8")
	  	  	body = json.loads(body_unicode)
	  	  	username = body["username"]
			password = body["password"]
		  except Exception as e:
		  	  return Response({"msg":"please verify input should not be empty"}) 
		  user = authenticate(username=username, password=password)
		  token=None;
		  if user is not None:
			 payload=jwt_payload_handler(user)
			 token=jwt_encode_handler(payload)
			 if user.is_active:
			 	user = UserM.objects.get(pk=user.id)
				user.profile.token =token
				user.save()
			 	if user.is_teacher:
			 	 	return Response({'id' : user.id,'token':token, 'username':user.username,'status':status.HTTP_200_OK, 'user':'teacher'})
			 	elif user.is_student:
					return Response({'id' : user.id,'token':token, 'username':user.username,'status':status.HTTP_200_OK, 'user':"student"})
				else:
				    return Response({'id' : user.id,'token':token, 'username':user.username,'status':status.HTTP_200_OK, 'user':"suoeruser"})
			 else:
				return Response({"success":"false"}) 
		  else:
			  return Response({'msg' : 'Invalid Credentials ! please enter valid input'},status.HTTP_404_NOT_FOUND)
