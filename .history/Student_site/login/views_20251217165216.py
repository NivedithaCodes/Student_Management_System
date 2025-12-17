from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import user,ClassRoom,Subject,AssignSubject,Syllabus,Timetable,Marks,Notification,Attendance
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q #for combining OR condition


  
def home_view(request):
    return render(request, "home.html")

def signup_view(request, popup=None):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        admission_no = request.POST.get("admission_no")
        dob = request.POST.get("dob")
        mobile = request.POST.get("mobile")

        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if user.objects.filter(email=email).exists():
            return render(request, 'home.html', {
                'popup': 'signup',
                'signup_error': 'User already exists!'
            })

        user.objects.create(
            admission_no=admission_no,
            name=name,
            email=email,
            dob=dob or None,
            mobile=mobile,
            password=password,
            role=role
        )

        messages.success(request, "Signup Successful")
        return redirect('login')

    return render(request, 'home.html')


def login_view(request, popup=None):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = user.objects.get(email=email)

            # Correct password check (your model stores plain passwords!)
            if user_obj.password == password:
                messages.success(request, "Login Successfully")

                # Store user_id in session manually
                request.session["user_id"] = user_obj.id
                request.session["role"] = user_obj.role

                # Redirect based on role
                if user_obj.role == "student":
                    return redirect('student')
                elif user_obj.role == "teacher":
                    return redirect('teacher')
                elif user_obj.role == "principal":
                    return redirect('principal')
                elif user_obj.role == "admin":
                    return redirect('principal')
            else:
                return render(request, 'home.html', {
                    'popup': 'login',
                    "login_error": "Incorrect Password"
                })

        except user.DoesNotExist:
            return render(request, 'home.html', {
                'popup': 'login',
                "login_error": "User Not Found"
            })

    return render(request, 'home.html')

def student_view(request):
    # 1. Check login session
    if "user_id" not in request.session:
        return redirect('login')

    # 2. Get logged-in user
    logged_in_user = user.objects.get(id=request.session["user_id"])

    # 3. Allow only students
    if logged_in_user.role != "student":
        return redirect('login')

    # 4. GET the selected tab
    tab = request.GET.get("tab", "dashboard")

    # 5. Add required context
    context = {
        # "user": logged_in_user,
        "tab": tab,
        'role': logged_in_user.role, # Pass role for sidebar
        
    }

    return render(request, "StudentPages/student.html", context)


# def teacher_view(request):
#     return render(request, "teacher_page.html")

# DASHBOARD / PRINCIPAL PAGE

def principal_view(request):
    # 1. Check login session
    if "user_id" not in request.session:
        return redirect('login')

    # 2. Get the logged-in user
    logged_in_user = user.objects.get(id=request.session["user_id"])

    # 3. Get the tab
    tab = request.GET.get("tab", "dashboard")

    # 4. Totals for dashboard
    total_students = user.objects.filter(role="student").count()
    total_teachers = user.objects.filter(role="teacher").count()
    total_subjects = Subject.objects.count()
   
    # 5. Prepare context
    context = {
        "tab": tab,
        "users_admin": user.objects.filter(role="admin"),
        "users_teacher": user.objects.filter(role="teacher"),
        "users_student": user.objects.filter(role="student"),
        "classes": ClassRoom.objects.all(),
        "subjects": AssignSubject.objects.all(),
        "subjects_list": Subject.objects.all(),   
        "syllabi": Syllabus.objects.all(),
        "timetables": Timetable.objects.all(),

        # Totals
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_subjects": total_subjects,

        # Pass the logged-in user for role-based sidebar
        # "user": logged_in_user,
        'role': logged_in_user.role,
    }
    return render(request, "PrincipalPages/principal.html", context)

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('home')

def profile_view(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect('login')

    u = user.objects.get(id=request.session["user_id"])

    context = {
        "user": u
    }

    return render(request, "base/profile.html", context)


def edit_profile_view(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect('login')

    u = user.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        u.name = request.POST.get("name")
        u.email = request.POST.get("email")
        u.mobile = request.POST.get("mobile")
        u.dob = request.POST.get("dob")

        # Handle photo upload
        if "photo" in request.FILES:
            u.photo = request.FILES["photo"]

        u.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")  # Redirect to profile page after edit

    context = {"user": u}
    return render(request, "base/edit_profile.html", context)

# ---------- CRUD actions for admin dashboard ----------
def add_admin(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # basic duplicate email protection
        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/principal/?tab=admin')

        user.objects.create(
            name=name,
            email=email,
            password=password,
            role="admin"
        )
    return redirect('/principal/?tab=admin') # redirect only after POST

def add_teacher(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")

        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/principal/?tab=teacher')

        user.objects.create(
            name=name,
            email=email,
            password="teacher@123",   # default password; you can change to posted password if you add it in the form
            role="teacher",
            subject=subject
        )
    return redirect('/principal/?tab=teacher')

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        class_id = request.POST.get("class_name")
        admission_no = request.POST.get("admission_no")
        
        # Check if email already exists
        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/principal/?tab=student')
        
        # Check if admission number already exists
        if admission_no and user.objects.filter(admission_no=admission_no).exists():
            messages.error(request, "Admission number already exists")
            return redirect('/principal/?tab=student')
        
        classroom = ClassRoom.objects.get(id=class_id)
        

        user.objects.create(
            name=name,
            admission_no=admission_no,
            email=email,
            password="student@123",
            role="student",
            class_name=classroom

        )
        messages.success(request, "Student added successfully!")
    return redirect('/principal/?tab=student')

def edit_user(request, id):
    u = get_object_or_404(user, id=id)

    if request.method == "POST":
        u.name = request.POST.get("name")
        u.email = request.POST.get("email")
        # if password field present, update it
        pwd = request.POST.get("password")
        if pwd:
            u.password = pwd

        # role-specific fields
        if u.role == "teacher":
            u.subject = request.POST.get("subject")
            u.save()
            return redirect('/principal/?tab=teacher')
        elif u.role == "student":
            u.class_name = request.POST.get("class")
            u.save()
            return redirect('/principal/?tab=student')
        elif u.role == "admin" :
            u.save()
            return redirect('/principal/?tab=admin')


    # GET -> render small edit page
    return render(request, "PrincipalPages/edit_user.html", {"user": u})

def delete_user(request, id):
    u = get_object_or_404(user, id=id)
    u.delete()

    # role-specific fields
    
    if u.role == "teacher":
        return redirect('/principal/?tab=teacher')
    elif u.role == "student":
        return redirect('/principal/?tab=student')
    elif u.role == "admin" :
            return redirect('/principal/?tab=admin')
    # return redirect('add_admin')

# CLASS MANAGEMENT
 
def add_class(request):
    # class_teacher= user.objects.filter(role='teacher')
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        section = request.POST.get("section") or None  
        max_strength = request.POST.get('max_strength') or None
        teacher_id = request.POST.get("class_teacher") or None
        class_teacher = user.objects.get(id=teacher_id) if teacher_id else None
        ClassRoom.objects.create(class_name=class_name, section=section,max_strength=max_strength,class_teacher=class_teacher)
        return redirect("/principal/?tab=class") 
    return redirect("/principal/?tab=class") 
    
def edit_class(request, id):
    cls = get_object_or_404(ClassRoom, id=id)
    users_teacher = user.objects.filter(role="teacher")

    if request.method == "POST":
        cls.class_name = request.POST.get("class_name")
        cls.section = request.POST.get("section") or None
        cls.max_strength = request.POST.get("max_strength") or None

        # update class_teacher 
        teacher_id = request.POST.get("class_teacher")
        if teacher_id:
            try:
                cls.class_teacher = user.objects.get(id=teacher_id)

            except user.DoesNotExist:
                cls.class_teacher = None
        else:
            cls.class_teacher = None

        cls.save()
        return redirect("/principal/?tab=class")   

    return render(request, "PrincipalPages/edit_class.html", {"cls": cls,"users_teacher": users_teacher})


def delete_class(request, id):
    cls = get_object_or_404(ClassRoom, id=id)
    cls.delete()
    return redirect("/principal/?tab=class")  

# SUBJECT MANAGEMENT

def add_only_subject(request):
    if request.method == "POST":
        Subject.objects.create(
            subject_name=request.POST.get("subject_name"),
            subject_code=request.POST.get("subject_code"),
        )
    return redirect("/principal/?tab=subject")

def edit_subject_base(request, id):
    sub = get_object_or_404(Subject, id=id)

    if request.method == "POST":
        sub.subject_name = request.POST.get("subject_name")
        sub.subject_code = request.POST.get("subject_code")
        sub.save()
        return redirect("/principal/?tab=subject")

    return render(request, "PrincipalPages/edit_subject_base.html", {"sub": sub})

def delete_subject_base(request, id):
    sub = get_object_or_404(Subject, id=id)
    sub.delete()
    return redirect("/principal/?tab=subject")


# ASSIGN SUBJECT MANAGEMENT
def assign_subject(request):
    if request.method == "POST":
        # subject_name = request.POST.get("subject_name")
        subject_id = request.POST.get("subject")
        assigned_class_id = request.POST.get("assigned_class")
        teacher_id = request.POST.get("teacher")

        # basic validation
        if not subject_id or not assigned_class_id:
            messages.error(request, "Subject name and class are required.")
            return redirect("/principal/?tab=assign")

        assigned_class = ClassRoom.objects.get(id=assigned_class_id)
        teacher_obj = user.objects.get(id=teacher_id) if teacher_id else None

        AssignSubject.objects.create(
            subject=Subject.objects.get(id=subject_id),
            assigned_class=assigned_class,
            teacher=teacher_obj,
        )
    return redirect("/principal/?tab=assign")


def edit_subject(request, id):
    sub = get_object_or_404(AssignSubject, id=id)
    if request.method == "POST":
        subject_id = request.POST.get("subject")
        if subject_id:
            sub.subject = Subject.objects.get(id=subject_id)
        class_id = request.POST.get("assigned_class")
        teacher_id = request.POST.get("teacher")
        if class_id:
            sub.assigned_class = ClassRoom.objects.get(id=class_id)
        sub.teacher = user.objects.get(id=teacher_id) if teacher_id else None
        sub.save()
        return redirect("/principal/?tab=assign") 
    context = {
        "subject": sub,
        "classes": ClassRoom.objects.all(),
        "users_teacher": user.objects.filter(role="teacher"),
        "subjects_list": Subject.objects.all(), 
    }
    return render(request, "PrincipalPages/edit_subject.html", context)



def delete_subject(request, id):
    sub = get_object_or_404(AssignSubject, id=id)
    sub.delete()
    return redirect("/principal/?tab=assign") 


# SYLLABUS MANAGEMENT
def add_syllabus(request):
    if request.method == "POST":
        class_room_id = request.POST.get("class_room")
        subject_id = request.POST.get("subject")
        syllabus_file = request.FILES.get("syllabus_file")

        if not class_room_id or not subject_id or not syllabus_file:
            messages.error(request, "All fields required.")
            return redirect("/principal/?tab=syllabus")

        class_room = ClassRoom.objects.get(id=class_room_id)
        subject = Subject.objects.get(id=subject_id)

        Syllabus.objects.create(
            class_room=class_room,
            subject=subject,
            syllabus_file=syllabus_file
        )
    return redirect("/principal/?tab=syllabus")


def edit_syllabus(request, id):
    syllabus = get_object_or_404(Syllabus, id=id)

    if request.method == "POST":
        class_room_id = request.POST.get("class_room")
        subject_id = request.POST.get("subject")
        if class_room_id:
            syllabus.class_room = ClassRoom.objects.get(id=class_room_id)
        if subject_id:
            syllabus.subject = Subject.objects.get(id=subject_id)

        if request.FILES.get("syllabus_file"):
            syllabus.syllabus_file = request.FILES.get("syllabus_file")

        syllabus.save()
        return redirect("PrincipalPages//principal/?tab=syllabus")

    context = {
        "syllabus": syllabus,
        "classes": ClassRoom.objects.all(),
        "subjects": Subject.objects.all(),
    }
    return render(request, "PrincipalPages/edit_syllabus.html", context)


def delete_syllabus(request, id):
    syllabus = get_object_or_404(Syllabus, id=id)
    syllabus.delete()
    messages.success(request, "Syllabus deleted successfully!")
    return redirect("/principal/?tab=syllabus")

def add_timetable(request):
    if request.method == "POST":
        class_id = request.POST.get("class_room")
        timetable_file = request.FILES.get("timetable_file")

        if not class_id or not timetable_file:
            messages.error(request, "Class and file are required.")
            return redirect("/principal/?tab=timetable")

        class_room = ClassRoom.objects.get(id=class_id)

        Timetable.objects.create(
            class_room=class_room,
            timetable_file=timetable_file
        )

    return redirect("/principal/?tab=timetable")

def edit_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)

    if request.method == "POST":
        class_id = request.POST.get("class_room")
        file = request.FILES.get("timetable_file")

        timetable.class_room = ClassRoom.objects.get(id=class_id)

        if file:
            timetable.timetable_file = file

        timetable.save()

        return redirect("/principal/?tab=timetable")

    context = {
        "timetable": timetable,
        "classes": ClassRoom.objects.all(),
    }
    return render(request, "PrincipalPages/edit_timetable.html", context)

def delete_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    timetable.delete()
    return redirect("/principal/?tab=timetable")

def settings_view(request):
    if "user_id" not in request.session:
        return redirect('login')

    u = user.objects.get(id=request.session["user_id"])

    return render(request, "base/settings.html", {"user": u})

def change_password(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect("login")

    u = user.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # 1️ Check current password (plain text)
        if old_password != u.password:
            messages.error(request, "❌ Current password is incorrect")
            return redirect("change_password")

        # 2️ Check new password matches confirm
        if new_password != confirm_password:
            messages.error(request, "❌ New passwords do not match")
            return redirect("change_password")

        # 3️ check minimum length
        if len(new_password) < 4:
            messages.error(request, "❌ Password must be at least 4 characters")
            return redirect("change_password")

        # 4️ Save new password directly (plain text)
        u.password = new_password
        u.save()

        messages.success(request, "✔ Password changed successfully!")
        return redirect("settings")

    return render(request, "base/change_password.html")


# Teacher Dasboard
 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import json


def teacher_view(request):
    if "user_id" not in request.session:
        return redirect('login')

    logged_in_user = user.objects.get(id=request.session["user_id"])
    if logged_in_user.role != "teacher":
        return redirect('login')

    tab = request.GET.get("tab", "attendance")

    # Classes where teacher is class teacher
    class_teacher_classes = ClassRoom.objects.filter(class_teacher=logged_in_user)

    # Classes where teacher is subject teacher
    assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)
    subject_classes = ClassRoom.objects.filter(id__in=assigned_subjects.values_list('assigned_class', flat=True))

    # All classes relevant for this teacher
    relevant_classes = (class_teacher_classes | subject_classes).distinct()

    # Students in each class
    # students_by_class = {}
    # for cls in relevant_classes:
    #     students_by_class[cls.id] = list(user.objects.filter(role='student', class_name=cls).order_by('name'))
    
    students_by_class = {}

    for cls in relevant_classes:
        students = user.objects.filter(
           role='student',
           class_name=cls
        ).values(
           "id",
           "name",
           "admission_no"
    )

    students_by_class[cls.id] = list(students)


    # Map: assign_subject_id -> student_ids
    subject_students_map = {}
    for assign in assigned_subjects:
        subject_students_map[assign.id] = list(user.objects.filter(role='student', class_name=assign.assigned_class).values_list('id', flat=True))

    # Which subjects can be marked by this teacher per class
    markable_subject_map = {}
    for cls in relevant_classes:
        subjects_in_class = AssignSubject.objects.filter(assigned_class=cls)
        markable_subjects = []
        for subj in subjects_in_class:
            if subj.teacher == logged_in_user or cls.class_teacher == logged_in_user:
                markable_subjects.append(subj.id)
        markable_subject_map[cls.id] = markable_subjects

    # List of class IDs where teacher is class teacher (for JS logic)
    class_teacher_ids = list(class_teacher_classes.values_list('id', flat=True))
     
    context = {
        "tab": tab,
        "classes": relevant_classes,
        "subjects": assigned_subjects,
        # "students_by_class": students_by_class,
        "students_by_class": json.dumps(students_by_class),
        "subject_students_map": subject_students_map,
        "markable_subject_map": markable_subject_map,
        "class_teacher_ids": class_teacher_ids,
        "role": logged_in_user.role,
        "user_id": logged_in_user.id,
        "today": timezone.localdate().strftime('%Y-%m-%d'),
        "user": logged_in_user,
   
    }
    return render(request, "TeacherPages/teacher.html", context)

from datetime import datetime
from django.utils import timezone


from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Attendance, user, AssignSubject, ClassRoom
from datetime import datetime

def submit_attendance(request):
    if request.method != "POST":
        return redirect('teacher')

    if "user_id" not in request.session:
        return redirect('login')
    
    logged_in_user = user.objects.get(id=request.session["user_id"])
    if logged_in_user.role != "teacher":
        return redirect('login')

    class_id = request.POST.get('class_id')
    assign_subject_id = request.POST.get('subject_id')
    date_str = request.POST.get('date') or timezone.localdate().isoformat()

    cls = get_object_or_404(ClassRoom, id=class_id)
    assign_obj = get_object_or_404(AssignSubject, id=assign_subject_id)

    # Permission check
    if not (cls.class_teacher == logged_in_user or assign_obj.teacher == logged_in_user):
        return redirect('teacher')

    try:
        attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        attendance_date = timezone.localdate()

    # Remove existing attendance
    Attendance.objects.filter(subject=assign_obj, date=attendance_date, student__class_name=cls).delete()

    # Mark attendance
    students_in_class = user.objects.filter(role='student', class_name=cls)
    total_present = 0
    total_absent = 0
    for student in students_in_class:
        present_field = f"present_{student.id}"
        status = "Present" if request.POST.get(present_field) in ("on", "present", "1") else "Absent"
        Attendance.objects.create(student=student, subject=assign_obj, date=attendance_date, status=status)
        if status == "Present":
            total_present += 1
        else:
            total_absent += 1
    
        # Fetch attendance again for summary display
    attendance_qs = Attendance.objects.filter(
        subject=assign_obj,
        date=attendance_date,
        # student__in=students_in_class
    ).select_related('student')

    # Map: student_id -> attendance object
    # attendance_map = {
    #     att.student_id: att for att in attendance_qs
    # }
    attendance_map = {}
    for att in attendance_qs:
        attendance_map[att.student.admission_no] = att.status.strip()


    students_with_attendance = []
    for stu in students_in_class:
     students_with_attendance.append({
        "student": stu,                      # student object
        "status": attendance_map.get(stu.id, "Not Marked")
    })

    context = {
        "class_name": cls.class_name,
        "section": cls.section,
        "subject": assign_obj.subject.subject_name,
        "date": attendance_date,
        "total_present": total_present,
        "total_absent": total_absent,
        "students": students_in_class,
        "attendance_map": attendance_map, 
        "students_with_attendance": students_with_attendance,
    }

    return render(request, "TeacherPages/attendance_summary.html", context)



# def submit_attendance(request):
#     if request.method != "POST":
#         return redirect('teacher')

#     if "user_id" not in request.session:
#         return redirect('login')

#     logged_in_user = user.objects.get(id=request.session["user_id"])
#     if logged_in_user.role != "teacher":
#         return redirect('login')

#     class_id = request.POST.get('class_id')
#     assign_subject_id = request.POST.get('subject_id')
#     date_str = request.POST.get('date') or timezone.localdate().isoformat()

#     cls = get_object_or_404(ClassRoom, id=class_id)
#     assign_obj = get_object_or_404(AssignSubject, id=assign_subject_id)
    
#     # Check: subject actually belongs to the class
#     if assign_obj.assigned_class != cls:
#         return redirect('teacher')

#     # Permission check: must be class teacher or subject teacher
#     if not (cls.class_teacher == logged_in_user or assign_obj.teacher == logged_in_user):
#         return redirect('teacher')

#     # Parse date
#     try:
#         attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except:
#         attendance_date = timezone.localdate()

#     # Remove existing attendance for this subject+date
#     Attendance.objects.filter(
#     subject=assign_obj,
#     date=attendance_date,
#     student__class_name=cls
#     ).delete()
  

#     # Mark attendance
#     students_in_class = user.objects.filter(role='student', class_name=cls)
#     for student in students_in_class:
#         present_field = f"present_{student.id}"
#         status = "Present" if request.POST.get(present_field) in ("on", "present", "1") else "Absent"
#         Attendance.objects.create(student=student, subject=assign_obj, date=attendance_date, status=status)

#     # return redirect('/teacher/?tab=attendance')
#     return redirect(f"{reverse('teacher')}?tab=attendance")



 
from django.http import JsonResponse
from .models import Attendance, user, AssignSubject, ClassRoom
from django.shortcuts import get_object_or_404

def get_attendance(request):
    class_id = request.GET.get('class_id')
    subject_id = request.GET.get('subject_id')
    date_str = request.GET.get('date')

    if not (class_id and subject_id and date_str):
        return JsonResponse({"error": "Missing parameters"}, status=400)

    cls = get_object_or_404(ClassRoom, id=class_id)
    assign_obj = get_object_or_404(AssignSubject, id=subject_id)
    
    try:
        from datetime import datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return JsonResponse({"error": "Invalid date"}, status=400)

    # Students in the class
    students = user.objects.filter(role='student', class_name=cls)
    attendance_data = []
    for stu in students:
        att = Attendance.objects.filter(student=stu, subject=assign_obj, date=date_obj).first()
        attendance_data.append({
            "id": stu.id,
            "name": stu.name,
            "admission_no": stu.admission_no,
            "status": att.status if att else "Not Marked"
        })

    return JsonResponse({"students": attendance_data})

# def view_attendance_dashboard(request):
#     if "user_id" not in request.session:
#         return redirect('login')

#     logged_in_user = user.objects.get(id=request.session["user_id"])
#     if logged_in_user.role != "teacher":
#         return redirect('login')

#     # Classes where teacher is class teacher
#     class_teacher_classes = ClassRoom.objects.filter(class_teacher=logged_in_user)

#     # Classes where teacher is subject teacher
#     assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)
#     subject_classes = ClassRoom.objects.filter(id__in=assigned_subjects.values_list('assigned_class', flat=True))

#     # All classes relevant for this teacher
#     relevant_classes = (class_teacher_classes | subject_classes).distinct()

#     # Students in each class
#     students_by_class = {}
#     for cls in relevant_classes:
#         students = user.objects.filter(
#             role='student',
#             class_name=cls
#         ).values(
#             "id", "name", "admission_no"
#         )
#         students_by_class[cls.id] = list(students)

#     # Only needed for view (marking optional)
#     markable_subject_map = {}
#     for cls in relevant_classes:
#         subjects_in_class = AssignSubject.objects.filter(assigned_class=cls)
#         markable_subjects = []
#         for subj in subjects_in_class:
#             if subj.teacher == logged_in_user or cls.class_teacher == logged_in_user:
#                 markable_subjects.append(subj.id)
#         markable_subject_map[cls.id] = markable_subjects

#     context = {
#         "classes": relevant_classes,
#         "subjects": assigned_subjects,
#         "students_by_class": json.dumps(students_by_class),
#         "markable_subject_map": markable_subject_map,
#         "class_teacher_ids": list(class_teacher_classes.values_list('id', flat=True)),
#         "today": timezone.localdate().strftime('%Y-%m-%d'),
#         "user": logged_in_user,
#         # "view_only": True,

#     }
#     return render(request, "TeacherPages/teacher_attendance.html", context)

def view_attendance_dashboard(request):
    logged_in_user = user.objects.get(id=request.session.get("user_id"))
    if logged_in_user.role != "teacher":
        return redirect('login')

    class_teacher_classes = ClassRoom.objects.filter(class_teacher=logged_in_user)
    assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)
    subject_classes = ClassRoom.objects.filter(id__in=assigned_subjects.values_list('assigned_class', flat=True))
    relevant_classes = (class_teacher_classes | subject_classes).distinct()

    students_by_class = {}
    for cls in relevant_classes:
        students = user.objects.filter(role='student', class_name=cls).values("id","name","admission_no")
        students_by_class[cls.id] = list(students)

    markable_subject_map = {}
    for cls in relevant_classes:
        subjects_in_class = AssignSubject.objects.filter(assigned_class=cls)
        markable_subjects = [subj.id for subj in subjects_in_class if subj.teacher == logged_in_user or cls.class_teacher == logged_in_user]
        markable_subject_map[cls.id] = markable_subjects

    # ✅ GET parameters for summary
    selected_class = request.GET.get('class_id')
    selected_subject = request.GET.get('subject_id')
    selected_date = request.GET.get('date')

    context = {
        "classes": relevant_classes,
        "subjects": assigned_subjects,
        "students_by_class": json.dumps(students_by_class),
        "markable_subject_map": markable_subject_map,
        "class_teacher_ids": list(class_teacher_classes.values_list('id', flat=True)),
        "today": timezone.localdate().strftime('%Y-%m-%d'),
        "user": logged_in_user,
        "selected_class": selected_class,
        "selected_subject": selected_subject,
        "selected_date": selected_date,
        "view_only": True,  # disables checkboxes
    }
    return render(request, "TeacherPages/teacher_attendance.html", context)

# View Student

def view_students(request):
    logged_user = user.objects.get(id=request.session.get("user_id"))

    if logged_user.role != "teacher":
        return redirect("login")

    filter_class = request.GET.get("class")

    # Gather all teacher dashboard context as in teacher_view
    class_teacher_classes = ClassRoom.objects.filter(class_teacher=logged_user)
    assigned_subjects = AssignSubject.objects.filter(teacher=logged_user)
    subject_class_ids = assigned_subjects.values_list("assigned_class", flat=True)

    # Students
    class_teacher_class = class_teacher_classes.first()
    class_teacher_students = user.objects.filter(
        role="student",
        class_name=class_teacher_class
    ) if class_teacher_class else user.objects.none()

    subject_teacher_students = user.objects.filter(
        role="student",
        class_name_id__in=subject_class_ids
    ).exclude(class_name=class_teacher_class) if class_teacher_class else user.objects.filter(
        role="student",
        class_name_id__in=subject_class_ids
    )

    # Apply filter
    if filter_class:
        class_teacher_students = class_teacher_students.filter(class_name_id=filter_class)
        subject_teacher_students = subject_teacher_students.filter(class_name_id=filter_class)

    context = {
        "tab": "view_students",   # keeps the tab active
        "classes": class_teacher_classes | ClassRoom.objects.filter(id__in=subject_class_ids),
        "class_teacher_students": class_teacher_students,
        "subject_teacher_students": subject_teacher_students,
        "class_teacher_class": class_teacher_class,
        "all_classes": ClassRoom.objects.filter(id__in=subject_class_ids) | class_teacher_classes,
        "filter_class": filter_class,
        "role": logged_user.role,
        "user_id": logged_user.id,
        "today": timezone.localdate(),
    }

    # Render teacher dashboard template (teacher.html)
    return render(request, "TeacherPages/teacher.html", context)



def student_profile_view(request, student_id):
    try:
        student = user.objects.get(id=student_id, role='student')
    except user.DoesNotExist:
        return redirect('teacher')  # fallback, or you can show 404

    context = {
        'student': student
    }
    return render(request, "StudentPages/student_profile.html", context)


# @login_required
# def mark_attendance(request):
#     if request.method == "POST":
#         class_id = request.POST.get("class_id")
#         date = request.POST.get("date")

#         students = user.objects.filter(role="student" ,assigned_class_id=class_id)

#         context = {
#             "students": students,
#             "class_id": class_id,
#             "date": date,
#         }
#         return render(request, "mark_attendance.html", context)

#     return redirect("teacher_dashboard")

# @login_required
# def submit_attendance(request):
#     if request.method == "POST":
#         class_id = request.POST.get("class_id")
#         date = request.POST.get("date")

#         for key, value in request.POST.items():
#             if key.startswith("student_"):
#                 student_id = key.split("_")[1]
#                 status = value

#                 Attendance.objects.create(
#                     student_id=student_id,
#                     date=date,
#                     status=status,
#                 )

#         messages.success(request, "Attendance submitted successfully.")
#         return redirect("teacher_dashboard")

#     return redirect("teacher_dashboard")

# @login_required
# def add_marks(request):
#     if request.method == "POST":
#         subject_id = request.POST.get("subject_id")
#         exam_name = request.POST.get("exam_name")

#         subject_obj = AssignSubject.objects.get(id=subject_id)

#         students = user.objects.filter(
#             role="student",
#             assigned_class=subject_obj.assigned_class
#         )

#         context = {
#             "students": students,
#             "exam_name": exam_name,
#             "subject_id": subject_id,
#         }
#         return render(request, "add_marks.html", context)

#     return redirect("teacher_dashboard")

# @login_required
# def submit_marks(request):
#     if request.method == "POST":
#         exam_name = request.POST.get("exam_name")
#         subject_id = request.POST.get("subject_id")

#         for key, value in request.POST.items():
#             if key.startswith("student_"):
#                 student_id = key.split("_")[1]
#                 mark = value

#                 Marks.objects.create(
#                     student_id=student_id,
#                     subject_id=subject_id,
#                     exam_name=exam_name,
#                     marks=mark,
#                 )

#         messages.success(request, "Marks added successfully.")
#         return redirect("teacher_dashboard")

#     return redirect("teacher_dashboard")

# @login_required
# def send_notification(request):
#     if request.method == "POST":
#         message = request.POST.get("message")

#         Notification.objects.create(
#             sender=request.user,
#             receiver_role="admin",
#             message=message,
#         )

#         messages.success(request, "Notification sent to Admin.")
#         return redirect("teacher_dashboard")

#     return HttpResponse("Invalid request")


 
