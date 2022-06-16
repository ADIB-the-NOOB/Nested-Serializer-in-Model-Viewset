from functools import partial
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Student, User
from .serializers import StudentSerializer, UserSerializer, UpdateStudentSerializer
from .custom_mixin import GetSerializerClassMixin, PermissionPolicyMixin


class StudentAPIView(GetSerializerClassMixin, viewsets.ModelViewSet):

    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    
    # def get_object(self, queryset=None, **kwargs):
    #     id = self.kwargs.get('pk')
    #     return get_object_or_404(Student, id=id)

    def get_queryset(self):
        return Student.objects.all()

    def update(self, request, pk=None):
        
        user_data = request.data.get('user')
        # print(user_data)
        student_obj = Student.objects.get(id=pk)
        user_obj = User.objects.get(id=student_obj.user.id)
        print(user_obj)

        
        user_obj.username = user_data.get('username', user_obj.username)
        user_obj.email = user_data.get('email', user_obj.email)
        user_obj.first_name = user_data.get('first_name', user_obj.first_name)
        user_obj.last_name = user_data.get('last_name', user_obj.last_name)
        user_obj.save()

        student_obj.semester = request.data.get('semester', student_obj.semester)
        student_obj.section = request.data.get('section', student_obj.section)
        student_obj.student_id = request.data.get('student_id', student_obj.student_id)
        student_obj.save()
        print(user_obj.last_name)

        serializer = StudentSerializer(data=request.data, partial=True)
        serializer.is_valid()
        return Response({'data': serializer.data})

# class StudentAPIView(viewsets.ViewSet):
#     queryset = Student.objects.all()

#     def list(self, request):
#         serializer_class = StudentSerializer(self.queryset, many=True)
#         return Response({
#             'data': serializer_class.data
#         })

#     def retrieve(self, request, pk=None):
#         student = get_object_or_404(self.queryset, pk=pk)
#         serializer_class = StudentSerializer(student)
#         return Response({
#             'data': serializer_class.data
#         })


