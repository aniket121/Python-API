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
from django.conf import settings
import uuid
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

username = "fry"
password = "password_yo"
full_name = "Philip J Fry"
#from elasticsearch_dsl import Q


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your views here.
class PaginatedState(APIView):
	 @staticmethod
	 def CommomState(paginatedData,pageNumbers):
	 	 if paginatedData.has_next() and paginatedData.has_previous():
	  	  	pageNumbers.append({'next_page':paginatedData.next_page_number(),'prev_page':paginatedData.previous_page_number()})
	  	 elif paginatedData.has_next():
	  	  	pageNumbers.append({'next_page':paginatedData.next_page_number(),'prev_page':'null'})
	  	 elif paginatedData.has_previous():
	  	  	pageNumbers.append({'next_page':'null','prev_page':paginatedData.previous_page_number()})
	  	 else:
	  	  	pageNumbers.append({'next_page':'null','prev_page':'null'})
class Users(PaginatedState,APIView):
	  
	  permission_classes = (permissions.IsAuthenticated,)
	  authentication_classes = (JSONWebTokenAuthentication,)
	  def get(self,request):
	  	  try:
		  	  ModelData=UserM.objects.all()
		  	  pageNumbers=[]
		  	  paginator=Paginator(ModelData,request.GET.get('limit', ''))
		  	  paginatedData=paginator.page(request.GET.get('page', ''))
		  	  PaginatedState.CommomState(paginatedData,pageNumbers)
		  	  serializeData = DynamicSerializer(paginatedData.object_list, many=True)
		  	  print serializeData
		  except Exception as e:
		  	  return Response({'msg':"Query parameter missing or went something wrong"})
	  	  return Response({'pages':pageNumbers,'next':paginatedData.has_next(),'prev':paginatedData.has_previous(),'range':str(paginatedData),"msg":"user list",'status' :status.HTTP_200_OK,'user':serializeData.data,'count':paginator.count})
	  def post(self, request):
	  	  body_unicode = request.body.decode("utf-8")
	  	  body = json.loads(body_unicode)
	  	  print "body==>",body
	  	  serializer = UserSerializer(data=body)
	  	  if serializer.is_valid():
	  	  	 UserObject=UserM.objects.create_user(username=body['username'], first_name=body['first_name'], last_name=body['last_name'],password=body['password'],email = body['email'],bio=body['bio'])

	  	  	 """
	  	  	 email = EmailMessage('Subject',get_template('../templates/email.html').render(
             Context({
	            'username': username,
	            'password': password,
	            'full_name': full_name
            })
            ), to=['aniket57gholap22@gmail.com'])
	  	  	 email.content_subtype = 'html'
	  	  	 email.send()
	  	  	 """
	  	  	 return Response({'success':'User registered successfully'},status.HTTP_200_OK)
	  	  else:
	  	  	return Response({'msg':'error occured while registration ! please enter valid input'},status.HTTP_404_NOT_FOUND)

class project(APIView):
      def post(self,request):
          body_unicode = request.body.decode("utf-8")
          body = json.loads(body_unicode)
          user_id=request.GET.get('user_id')
          project = Projects()
          if Projects.objects.filter(name=body['projectName']).exists():
             return Response({'msg':'Project alredy exits'},status.HTTP_200_OK)
          project.name = body['projectName']
          project.user_id=user_id
          project.save()
          allProject=Projects.objects.filter(user_id=user_id)
          jsondata = ProjectSerializer(allProject,many=True)
          return Response({'msg' : 'project added successfully','project' : jsondata.data},status.HTTP_200_OK)
      def get(self,request):
          user_id=request.GET.get('user_id')
          allProject=Projects.objects.filter(user_id=user_id)
          jsondata = ProjectSerializer(allProject,many=True)
          return Response({'project' : jsondata.data},status.HTTP_200_OK)
class Search(APIView):
	  def get(self,request):
	  	   searchInput=request.GET.get('search')
	  	   FilterRecords =UserM.objects.filter(Q(username__contains=searchInput) | Q(first_name__contains=searchInput))
	  	   #FilterRecords=userTrack.search().query(Q("match", username=searchInput) | Q("match", first_name=searchInput))
	  	   pageNumbers=[]
	  	   paginator=Paginator(FilterRecords,request.GET.get('limit', ''))
	  	   paginatedData=paginator.page(request.GET.get('page', ''))
	  	   PaginatedState.CommomState(paginatedData,pageNumbers)
	  	   serializer =DynamicSerializer(data=FilterRecords,many=True)
	  	   if serializer.is_valid():
	  	   	   
	  	   	   return Response({'user':serializer.data},status.HTTP_200_OK)
	  	   else: 
	  	   	   pass
	  	   	   logging.info('result successfully fetched')
	  	   	   return Response({'pages':pageNumbers,'next':paginatedData.has_next(),'prev':paginatedData.has_previous(),'range':str(paginatedData),"msg":"user list",'status' :status.HTTP_200_OK,'user':serializer.data,'count':paginator.count},status.HTTP_200_OK)
class Images(APIView):
      def post(self,request):
      	  fileList={}
          for file in request.FILES.getlist('file'):
	          fs = FileSystemStorage()
	          filename = fs.save(str(uuid.uuid4())+"/" + file.name, file)
	          uploaded_file_url = fs.url(filename)
	          fileList.update({file.name : settings.DEFAULT_PROTOCOL+"://"+settings.BASE_ADDRESS+uploaded_file_url})
          return Response({'url' : fileList},status.HTTP_200_OK)
                 
          
              
                 
          
	  
			
