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
    
    def get_object(self, queryset=None, **kwargs):
        id = self.kwargs.get('pk')
        return get_object_or_404(Student, id=id)

    def get_queryset(self):
        return Student.objects.all()

    def update(self, request, pk=None):
        
        user_data = request.data.pop('user')
        user_obj = User.objects.get(id=pk)

        serializer = UserSerializer(data=user_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        # print(user_obj)
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


