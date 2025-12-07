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
        return self.subject

 
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

# ======================================================
# NEW — ATTENDANCE (Required for Teacher Dashboard)
# ======================================================
class Attendance(models.Model):
    student = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    subject = models.ForeignKey(AssignSubject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # Present / Absent

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


# ======================================================
# NEW — MARKS (Required for Add Marks Feature)
# ===========================
class Marks(models.Model):
    student = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    subject = models.ForeignKey(AssignSubject, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.exam_name}"

# NOTIFICATIONS (Teacher → Admin)
    sender = models.ForeignKey(
        user,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_notifications"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_for_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification from {self.sender}"
❗ IMPORTANT FIX YOU NEEDED
In your AssignSubject model, you had:

python
Copy code
def __str__(self):
    return self.subject