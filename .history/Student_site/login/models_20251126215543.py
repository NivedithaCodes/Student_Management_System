# from django.db import models

# class user(models.Model):
#     admission_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
#     name = models.CharField(max_length=150)
#     email = models.EmailField(unique=True)
#     dob = models.DateField(null=True, blank=True)
#     mobile = models.CharField(max_length=20, null=True, blank=True)
#     password = models.CharField(max_length=255)

#     ROLE_CHOICES = (
#         ("student", "Student"),
#         ("parent", "Parent"),
#         ("teacher", "Teacher"),
#         ("principal", "Principal"),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)

#     def __str__(self):
#         return self.name
    
from django.db import models

class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20)   # admin / teacher / student
    class_name = models.CharField(max_length=20, blank=True, null=True)  # only for students
    subject = models.CharField(max_length=50, blank=True, null=True)     # only for teachers

    def __str__(self):
        return self.name


 
