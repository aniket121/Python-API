from rest_framework import permissions

class IsTeacherUserOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
    	try: 
           return request.user and request.user.is_teacher
        except:
           return False
class IsStudentUserOnly(permissions.BasePermission):
    """
    Allows access only to student users.
    """
    def has_permission(self, request, view):
    	try:
           return request.user and request.user.is_student
        except:
           return False