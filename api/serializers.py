from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Student
from rest_framework.response import Response

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = "__all__"

    
    def create(self, validated_data):
        user = validated_data.get('user')

        student_id = validated_data.get('student_id')
        semester = validated_data.get('semester')
        section = validated_data.get('section')

        user_obj = UserSerializer.create(UserSerializer(), validated_data=user)

        student_obj = Student.objects.create(
            user=user_obj, student_id=student_id,
            semester=semester, section=section)
        # print(validated_data)
        return student_obj



class UpdateStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = "__all__"


    def update(self, instance, validated_data):
        
        user_data = validated_data.get('user')
        if user_data is not None:
            user_obj = User.objects.get(id=instance.user.id)
            user = UserSerializer.update(self, instance=user_obj, validated_data=user_data)
            instance.user = user
        instance.semester = validated_data.get('semester', instance.semester)
        instance.section = validated_data.get('section', instance.section)
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.save()

        return instance