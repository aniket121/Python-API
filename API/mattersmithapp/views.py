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
from elasticsearch_dsl import Q


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

	  #permission_classes = (permissions.IsAuthenticated,)
	  #authentication_classes = (JSONWebTokenAuthentication,)
	  #authentication_classes = (JSONWebTokenAuthentication,)
	  #permission_classes = (permissions.IsAuthenticated,)
	  #serializer_class = UserSerializer
	  def get(self,request):
	  	  try:
		  	  ModelData=User.objects.all()
		  	  pageNumbers=[]
		  	  paginator=Paginator(ModelData,request.GET.get('limit', ''))
		  	  paginatedData=paginator.page(request.GET.get('page', ''))
		  	  PaginatedState.CommomState(paginatedData,pageNumbers)
		  	  serializeData = DynamicSerializer(paginatedData.object_list, many=True)
		  except Exception as e:
		  	  return Response({'msg':"Query parameter missing or went something wrong"})
	  	  return Response({'pages':pageNumbers,'next':paginatedData.has_next(),'prev':paginatedData.has_previous(),'range':str(paginatedData),"msg":"user list",'status' :status.HTTP_200_OK,'user':serializeData.data,'count':paginator.count})
	  def post(self, request):
	  	  body_unicode = request.body.decode("utf-8")
	  	  body = json.loads(body_unicode)
	  	  print "body==>",body
	  	  serializer = UserSerializer(data=body)
	  	  if serializer.is_valid():
	  	  	User.objects.create_user(username=body['username'], first_name=body['first_name'], last_name=body['last_name'],password=body['password'],email = body['email'])
	  	  	return Response({'success':'User registered successfully'},status.HTTP_200_OK)
	  	  else:
	  	  	return Response({'msg':'error occured while registration ! please enter valid input'},status.HTTP_404_NOT_FOUND)
class login(APIView):
	  permission_classes = (permissions.AllowAny,)

	  def post(self, request):
	  	  if request.method =="POST":
	  	  	 body_unicode = request.body.decode("utf-8")
	  	  	 body = json.loads(body_unicode)
			 username = body["username"]
			 password = body["password"]
			 user = authenticate(username=username, password=password)
			 token=None;
			 if user is not None:
			 	payload=jwt_payload_handler(user)
			 	token=jwt_encode_handler(payload)
			 	if user.is_active:
			 	 	user = User.objects.get(pk=user.id)
					user.profile.token =token
					user.save()
			 	 	if user.is_superuser and user.is_staff:
			 	 	   return Response({'id' : user.id,'token':token, 'username':user.username,'status':status.HTTP_200_OK, 'user':'superuser'})
			 	 	elif user.is_staff:
					    return Response({'id' : user.id,'token':token, 'username':user.username,'status':status.HTTP_200_OK, 'user':"admin"})
					else:
						return Response({'id' : user.id,'token':token, 'username':user.username,'status':status.HTTP_200_OK, 'user':"user"})
				else:
				     return Response({"success":"false"}) 
			 else:
			     return Response({'msg' : 'Invalid Credentials ! please enter valid input'},status.HTTP_404_NOT_FOUND)
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
	  	   #FilterRecords =User.objects.filter(Q(username__contains=searchInput) | Q(first_name__contains=searchInput))
	  	   FilterRecords=userTrack.search().query(Q("match", username=searchInput) | Q("match", first_name=searchInput))
	  	   pageNumbers=[]
	  	   paginator=Paginator(FilterRecords,request.GET.get('limit', ''))
	  	   paginatedData=paginator.page(request.GET.get('page', ''))
	  	   PaginatedState.CommomState(paginatedData,pageNumbers)
	  	   serializer =DynamicSerializer(data=FilterRecords,many=True)
	  	   if serializer.is_valid():
	  	   	   print "in if"
	  	   	   return Response({'user':serializer.data},status.HTTP_200_OK)
	  	   else:
	  	   	   print "in else"
	  	   	   return Response({'user':serializer.data},status.HTTP_200_OK)
           
	  
			
class Images(APIView):
      def post(self,request):
          user_id=request.GET.get('user_id')
          # TODO
          pass
                 
          
              
                 
          
	  
			
