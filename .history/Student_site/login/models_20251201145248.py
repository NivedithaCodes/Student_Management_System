from django.db import models

class user(models.Model):
    admission_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255)

    # Added nullable fields so we can store teacher subject and student class without breaking existing data
    class_name = models.CharField(max_length=50, null=True, blank=True)   # used for students
    subject = models.CharField(max_length=100, null=True, blank=True)     # used for teachers

    ROLE_CHOICES = (
        ("student", "Student"),
        ("parent", "Parent"),
        ("teacher", "Teacher"),
        ("principal", "Principal"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


 from django.db import models
from teacher.models import Teacher  # if you have a Teacher model

class ClassRoom(models.Model):
    class_name = models.CharField(max_length=50)   # e.g., 10
    section = models.CharField(max_length=10)      # e.g., A
    class_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    max_strength = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.class_name} {self.section}"


 
