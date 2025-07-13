# student/models.py
from django.db import models
from course.models import Course  # Import Course model

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    contact = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=150, blank=False)
    email = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)  # New Field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
