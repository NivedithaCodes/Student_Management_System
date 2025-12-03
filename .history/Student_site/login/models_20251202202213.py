# from django.db import models

# class user(models.Model):
#     admission_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
#     name = models.CharField(max_length=150)
#     email = models.EmailField(unique=True)
#     dob = models.DateField(null=True, blank=True)
#     mobile = models.CharField(max_length=20, null=True, blank=True)
#     password = models.CharField(max_length=255)

#     # Added nullable fields so we can store teacher subject and student class without breaking existing data
#     class_name = models.CharField(max_length=50, null=True, blank=True)   # used for students
#     subject = models.CharField(max_length=100, null=True, blank=True)     # used for teachers

#     ROLE_CHOICES = (
#         ("student", "Student"),
#         ("parent", "Parent"),
#         ("teacher", "Teacher"),
#         ("principal", "Principal"),
#         ("admin", "Admin"),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)

#     def __str__(self):
#         return self.name


# class ClassRoom(models.Model):
#     class_name = models.CharField(max_length=50)   # e.g., 10
#     section = models.CharField(max_length=10)      # e.g., A
#     class_teacher = models.ForeignKey(
#         user, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role':'teacher'},
#         related_name='classes'
#     )
#     academic_year = models.CharField(max_length=20, blank=True, null=True)
#     max_strength = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.class_name} {self.section}"


# class Subject(models.Model):
#     name = models.CharField(max_length=100)
#     class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(
#         user, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role':'teacher'},
#         related_name='subjects'
#     )

#     def __str__(self):
#         return f"{self.name} ({self.class_room})"


from django.db import models

 
# USER MODEL
 
class user(models.Model):
    admission_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255)

    class_name = models.CharField(max_length=50, null=True, blank=True)  
    subject = models.CharField(max_length=100, null=True, blank=True)    

    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("principal", "Principal"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


 
# CLASS MODEL
 
class ClassRoom(models.Model):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, null=True, blank=True)
    max_strength = models.IntegerField(null=True, blank=True)
    class_teacher = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True) 
    
    class_teacher = models.ForeignKey(
        user,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='class_teacher_for'
    )

    def __str__(self):
        return f"{self.class_name} {self.section}"


 
# SUBJECT MODEL  
 
# class Subject(models.Model):
#     subject_name = models.CharField(max_length=100)
#     assigned_class = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,related_name='subjects')
#     teacher = models.ForeignKey(
#         user, null=True, blank=True,
#         on_delete=models.SET_NULL,
#         related_name='subjects_assigned',
#         limit_choices_to={'role': 'teacher'},
#     )

#     def __str__(self):
#         return self.subject_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)
    subject_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"


 
# ASSIGN SUBJECT MODEL 
 
# class AssignSubject(models.Model):
#     teacher = models.ForeignKey(user, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
#     class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.teacher.name} - {self.subject.subject_name} ({self.class_room})"

class AssignSubject(models.Model):
    subject_name = models.CharField(max_length=100)
    assigned_class = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,related_name='subjects',null=True,blank=)
    teacher = models.ForeignKey(
        user, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='subjects_assigned',
        limit_choices_to={'role': 'teacher'},
    )

    def __str__(self):
        return self.subject_name

 
# SYLLABUS MODEL
 
class Syllabus(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,related_name='syllabi')
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='syllabi')
    syllabus_file = models.FileField(upload_to='syllabus/',null=True,blank=True)

    def __str__(self):
        return f"{self.class_room} - {self.subject}"


 
# TIMETABLE MODEL
 
class Timetable(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='timetables')
    timetable_file = models.FileField(upload_to='timetable/',null=True,blank=True)

    def __str__(self):
        return f"{self.class_room} – Timetable"
