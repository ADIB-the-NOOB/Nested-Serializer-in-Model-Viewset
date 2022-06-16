from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Student, User
from .serializers import StudentSerializer, UpdateStudentSerializer
from .custom_mixin import GetSerializerClassMixin

class StudentAPIView(GetSerializerClassMixin, viewsets.ModelViewSet):

    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    serializer_action_classes = {
        'retrieve': StudentSerializer,
        'create': StudentSerializer,
        'update': UpdateStudentSerializer,
        'partial_update': UpdateStudentSerializer
    }
    def get_queryset(self):
        return Student.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Student ID created!',
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        })

    def update(self, request, *args, **kwargs):
        student=self.get_object()
        serializer = self.get_serializer(instance=student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Student data updated!',
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        })

    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        student = self.get_object()
        user = User.objects.get(id=student.user.id)
        user.delete()
        student.delete()
        return Response({'message': 'student deleted'})


