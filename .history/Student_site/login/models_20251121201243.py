from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now_add=True)
    
