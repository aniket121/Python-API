from rest_framework import serializers
#from .models import User
from django.contrib.auth.models import User
from mattersmithapp.models import *


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserM
		fields = ('username','password','first_name','last_name','is_active','is_staff','email','bio','is_student','is_teacher')
                def get(self):
                    print "get serilazer"

class DynamicSerializer(UserSerializer):

    class Meta:
        model = UserM
        fields = (
            'first_name','first_name','last_name','is_active','is_staff','email','username','bio','is_student','is_teacher'
        )

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Projects
		fields = '__all__'
"""
class UserRolesSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserRoles
		fields = '__all__'
"""

