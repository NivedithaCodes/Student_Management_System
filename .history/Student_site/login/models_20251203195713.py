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

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)
    subject_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"


 
# ASSIGN SUBJECT MODEL 
    
class AssignSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,blank=True)
    # subject_name = models.CharField(max_length=100,null=True,blank=True)
    assigned_class = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,related_name='subjects',null=True,blank=True)
    teacher = models.ForeignKey(
        user, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='subjects_assigned',
        limit_choices_to={'role': 'teacher'},
    )

    def __str__(self):
        return self.subject_nam

 
# SYLLABUS MODEL
 
class Syllabus(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,related_name='syllabi')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='syllabi',null=True,blank=True)
    syllabus_file = models.FileField(upload_to='syllabus/',null=True,blank=True)

    def __str__(self):
        return f"{self.class_room} - {self.subject}"
    
# TIMETABLE MODEL
 
class Timetable(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='timetables')
    timetable_file = models.FileField(upload_to='timetable/',null=True,blank=True)

    def __str__(self):
        return f"{self.class_room} – Timetable"
