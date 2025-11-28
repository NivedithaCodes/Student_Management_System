from django.db import models

class User(models.Model):
    admission_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255)

    ROLE_CHOICES = (
        ("student", "Student"),
        ("parent", "Parent"),
        ("teacher", "Teacher"),
        ("principal", "Principal"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

