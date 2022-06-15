from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=15)
    section = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.first_name}-{self.student_id}"
