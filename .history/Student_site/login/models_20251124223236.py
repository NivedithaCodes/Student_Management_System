from django.db import models

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     age = models.IntegerField()
#     department = models.CharField(max_length=100)
#     joined_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class user(models.Model):
#     name=models.CharField(max_length=255)
#     email=models.CharField(max_length=255,unique=True)
#     password=models.CharField(max_length=255)

# class Profile(models.Model):
#     ROLE_CHOICES = [
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#         ('teacher', 'Teacher'),
#         ('principal', 'Principal'),
#     ]

#     user = models.OneToOneField(user, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)

#     def __str__(self):
#         return self.user.username

# class user(models.Model):
#     ROLE_CHOICES = (
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#         ('teacher', 'Teacher'),
#         ('principal', 'Principal'),
#     )

#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)

#     def __str__(self):
#         return self.name

class user(models.Model):
    # admission_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # dob = models.DateField()
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
