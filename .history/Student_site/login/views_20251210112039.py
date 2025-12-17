from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import user,ClassRoom,Subject,AssignSubject,Syllabus,Timetable,Marks,Notification,Attendance
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone

  
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
        
        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/principal/?tab=student')
        
        classroom = ClassRoom.objects.get(id=class_id)
        

        user.objects.create(
            name=name,
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

        # 1️⃣ Check current password (plain text)
        if old_password != u.password:
            messages.error(request, "❌ Current password is incorrect")
            return redirect("change_password")

        # 2️⃣ Check new password matches confirm
        if new_password != confirm_password:
            messages.error(request, "❌ New passwords do not match")
            return redirect("change_password")

        # 3️⃣ Optional: check minimum length
        if len(new_password) < 4:
            messages.error(request, "❌ Password must be at least 4 characters")
            return redirect("change_password")

        # 4️⃣ Save new password directly (plain text)
        u.password = new_password
        u.save()

        messages.success(request, "✔ Password changed successfully!")
        return redirect("settings")

    return render(request, "base/change_password.html")


# Teacher Dasboard

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import ClassRoom, AssignSubject, user, Attendance

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
    students_by_class = {}
    for cls in relevant_classes:
        students_by_class[cls.id] = list(user.objects.filter(role='student', class_name=cls).order_by('name'))

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
        "students_by_class": students_by_class,
        "subject_students_map": subject_students_map,
        "markable_subject_map": markable_subject_map,
        "class_teacher_ids": class_teacher_ids,
        "role": logged_in_user.role,
        "user_id": logged_in_user.id,
        "today": timezone.localdate(),

        "user": logged_in_user,
    }
    return render(request, "TeacherPages/teacher.html", context)

from datetime import datetime
from django.utils import timezone

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

    # Permission check: must be class teacher or subject teacher
    if not (cls.class_teacher == logged_in_user or assign_obj.teacher == logged_in_user):
        return redirect('teacher')

    # Parse date
    try:
        attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        attendance_date = timezone.localdate()

    # Remove existing attendance for this subject+date
    Attendance.objects.filter(subject=assign_obj, date=attendance_date).delete()

    # Mark attendance
    students_in_class = user.objects.filter(role='student', class_name=cls)
    for student in students_in_class:
        present_field = f"present_{student.id}"
        status = "Present" if request.POST.get(present_field) in ("on", "present", "1") else "Absent"
        Attendance.objects.create(student=student, subject=assign_obj, date=attendance_date, status=status)

    return redirect('/teacher/?tab=attendance')

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance, AssignSubject, ClassRoom, user

def view_attendance(request):
    if "user_id" not in request.session:
        return redirect('login')

    logged_in_user = user.objects.get(id=request.session["user_id"])
    if logged_in_user.role != "teacher":
        return redirect('login')

    # Classes where teacher is class teacher
    class_teacher_classes = ClassRoom.objects.filter(class_teacher=logged_in_user)

    # Subjects assigned to teacher
    assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)

    # For class teacher: show all subjects in their classes
    class_teacher_subjects = AssignSubject.objects.filter(assigned_class__in=class_teacher_classes)

    # Merge subjects (class teacher sees all subjects in their classes, subject teacher sees only their subjects)
    subjects_to_view = (class_teacher_subjects | assigned_subjects).distinct()

    # Attendance records
    attendance_records = Attendance.objects.filter(subject__in=subjects_to_view).order_by('-date')

    # For filter dropdowns
    classes = ClassRoom.objects.filter(id__in=subjects_to_view.values_list('assigned_class', flat=True).distinct())
    subjects = subjects_to_view

    context = {
        "attendance_records": attendance_records,
        "classes": classes,
        "subjects": subjects,
        "role": logged_in_user.role,
    }

    return render(request, "TeacherPages/view_attendance.html", context)

# def teacher_view(request):
#     if "user_id" not in request.session:
#         return redirect('login')

#     logged_in_user = user.objects.get(id=request.session["user_id"])

#     if logged_in_user.role != "teacher":
#         return redirect('login')

#     tab = request.GET.get("tab", "dashboard")

#     # Subjects this teacher teaches
#     assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)

#     # Classes this teacher is involved in (as class teacher or subject teacher)
#     class_teacher_class = ClassRoom.objects.filter(class_teacher=logged_in_user)
#     subject_teacher_classes = ClassRoom.objects.filter(
#         id__in=assigned_subjects.values_list("assigned_class", flat=True)
#     )

#     all_classes = (class_teacher_class | subject_teacher_classes).distinct()

#     context = {
#         "tab": tab,
#         "classes": all_classes,
#         "subjects": assigned_subjects,
#     }

#     return render(request, "TeacherPages/teacher.html", context)

# def submit_attendance(request):
#     if request.method != "POST":
#         return redirect('teacher')

#     if "user_id" not in request.session:
#         return redirect('login')

#     teacher = user.objects.get(id=request.session["user_id"])

#     class_id = request.POST.get("class_id")
#     assign_subject_id = request.POST.get("subject_id")
#     date_str = request.POST.get("date")

#     cls = get_object_or_404(ClassRoom, id=class_id)
#     subject_assign = get_object_or_404(AssignSubject, id=assign_subject_id)

#     # PERMISSION CHECK
#     if not (cls.class_teacher == teacher or subject_assign.teacher == teacher):
#         return redirect("teacher")

#     # Parse date
#     from datetime import datetime
#     try:
#         attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except:
#         attendance_date = timezone.localdate()

#     # Remove old attendance for this subject and date
#     Attendance.objects.filter(subject=subject_assign, date=attendance_date).delete()

#     # Students
#     students = user.objects.filter(role="student", class_name=cls)

#     # Save new
#     for s in students:
#         status = "Present" if request.POST.get(f"present_{s.id}") else "Absent"
#         Attendance.objects.create(student=s, subject=subject_assign, date=attendance_date, status=status)

#     return redirect("/teacher/?tab=attendance")

 
# def teacher_view(request):
#     # 1. Check session login
#     if "user_id" not in request.session:
#         return redirect('login')

#     # 2. Get the logged-in user
#     logged_in_user = user.objects.get(id=request.session["user_id"])

#     # 3. Allow only teachers
#     if logged_in_user.role != "teacher":
#         return redirect('login')

#     tab = request.GET.get("tab", "dashboard")

#     # 4. Subjects assigned to this teacher (AssignSubject instances)
#     assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)

#     # 5. Classes assigned to this teacher (via assigned_subjects)
#     assigned_classes = ClassRoom.objects.filter(
#         id__in=assigned_subjects.values_list('assigned_class', flat=True)
#     )

#     # Prepare students_by_class: { class_id: [student objects] }
#     students_by_class = {}
#     for cls in assigned_classes:
#         students_by_class[cls.id] = list(user.objects.filter(role='student', class_name=cls).order_by('name'))

#     # Prepare subject_students_map: { assignsubject_id: [student_id, ...] }
#     # A student is considered "in subject" if they belong to that class and subjects_assigned includes that assignobject
#     # This uses the AssignSubject relation to find students via the reverse 'subjects_assigned' if applicable.
#     # If you don't have a direct relation connecting student to an AssignSubject, adjust accordingly (this assumes
#     # student->subjects_assigned reverse FK exists from your models).
#     subject_students_map = {}
#     for a in assigned_subjects:
#         # students in the same class who are linked to this assignsubject via subjects_assigned (reverse related_name)
#         subject_students = user.objects.filter(
#             role='student',
#             class_name=a.assigned_class,
#             subjects_assigned__id=a.id
#         ).distinct().values_list('id', flat=True)
#         subject_students_map[a.id] = list(subject_students)

#     # Students relevant to teacher (merge class teacher students & subject students)
#     subject_students_all = user.objects.filter(
#         role='student',
#         class_name__in=assigned_classes
#     )
#     class_teacher_students = user.objects.filter(
#         role='student',
#         class_name__class_teacher=logged_in_user
#     )
#     students_combined = (subject_students_all | class_teacher_students).distinct()

#     # Build flagged list for any other uses
#     students_with_flag = []
#     for student in students_combined:
#         students_with_flag.append({
#             "student": student,
#             "is_class_student": student.class_name.class_teacher == logged_in_user
#         })

#     # Syllabus & timetables (as before)
#     syllabi = Syllabus.objects.filter(
#         subject__in=assigned_subjects.values_list('subject', flat=True),
#         class_room__in=assigned_classes
#     )
#     timetables = Timetable.objects.filter(class_room__in=assigned_classes)

#     context = {
#         "tab": tab,
#         "classes": assigned_classes,               # queryset of ClassRoom objects
#         "subjects": assigned_subjects,             # queryset of AssignSubject objects (id, subject, assigned_class, teacher)
#         "students_by_class": students_by_class,    # dict class_id -> list(student objects)
#         "subject_students_map": subject_students_map,  # dict assignsubject_id -> list(student_ids)
#         "users_student": students_with_flag,
#         "syllabi": syllabi,
#         "timetables": timetables,
#         "role": logged_in_user.role,
#     }

#     return render(request, "TeacherPages/teacher.html", context)


# # View to accept POST from template and store attendance
# def submit_attendance(request):
#     if request.method != "POST":
#         return redirect('teacher')

#     if "user_id" not in request.session:
#         return redirect('login')

#     logged_in_user = user.objects.get(id=request.session["user_id"])
#     if logged_in_user.role != "teacher":
#         return redirect('login')

#     # Expecting these POST fields: date (YYYY-MM-DD), class_id, assign_subject_id (subject assignment), and keys present_<student_id>=on
#     class_id = request.POST.get('class_id')
#     assign_subject_id = request.POST.get('subject_id')
#     date_str = request.POST.get('date') or timezone.localdate().isoformat()  # default to today

#     if not class_id or not assign_subject_id:
#         # invalid request
#         return redirect('teacher')

#     # Basic permission check: ensure teacher is permitted for this class/subject
#     assign_obj = get_object_or_404(AssignSubject, id=assign_subject_id)
#     cls = get_object_or_404(ClassRoom, id=class_id)
#     # teacher must be either the class teacher or the subject teacher
#     if not (assign_obj.teacher == logged_in_user or cls.class_teacher == logged_in_user):
#         # not allowed
#         return redirect('teacher')

#     # Get list of students in that class
#     students_in_class = user.objects.filter(role='student', class_name=cls)

#     # Save attendance: treat checked boxes as Present, others as Absent
#     # To avoid duplicates, delete any existing attendance for that date+subject+students (or update)
#     from datetime import datetime
#     try:
#         attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except Exception:
#         attendance_date = timezone.localdate()

#     # Optional: remove existing attendance entries for this subject+date to replace them
#     Attendance.objects.filter(subject=assign_obj, date=attendance_date).delete()

#     for student in students_in_class:
#         present_field = f"present_{student.id}"
#         status = "Present" if request.POST.get(present_field) in ("on", "present", "1") else "Absent"
#         Attendance.objects.create(student=student, subject=assign_obj, date=attendance_date, status=status)

#     # After saving redirect back to attendance tab
#     return redirect('/teacher/?tab=attendance')

# def teacher_view(request):
#     # 1. Check session login
#     if "user_id" not in request.session:
#         return redirect('login')

#     # 2. Get the logged-in user
#     logged_in_user = user.objects.get(id=request.session["user_id"])

#     # 3. Allow only teachers
#     if logged_in_user.role != "teacher":
#         return redirect('login')
 
#     tab = request.GET.get("tab", "dashboard")

#     # 4. Subjects assigned to this teacher
#     assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)

#     # 5. Classes assigned to this teacher
#     assigned_classes = ClassRoom.objects.filter(
#         id__in=assigned_subjects.values_list('assigned_class', flat=True)
#     )

#     # # 6. Students in assigned classes  
#     # students = user.objects.filter(
#     #     role='student',
#     #     class_name__in=assigned_classes.values_list("class_name", flat=True)
#     # )

#       # 6a. Students in subjects she teaches
#     subject_students = user.objects.filter(
#         role='student',
#         class_name__in=assigned_classes
#     )

#     # 6b. Students in classes where she is class teacher
#     class_teacher_students = user.objects.filter(
#         role='student',
#         class_name__class_teacher=logged_in_user
#     )

#     # 6c. Merge both and remove duplicates
#     students = (subject_students | class_teacher_students).distinct()

#     # 7. For template, mark if student is her class
#     students_with_flag = []
#     for student in students:
#         students_with_flag.append({
#             "student": student,
#             "is_class_student": student.class_name.class_teacher == logged_in_user
#         })

#     # 8. Syllabus  
#     syllabi = Syllabus.objects.filter(
#         subject__in=assigned_subjects.values_list('subject', flat=True),
#         class_room__in=assigned_classes   
#     )

#     # 9. Timetable (same issue, FIXED)
#     timetables = Timetable.objects.filter(
#         class_room__in=assigned_classes   
#     )

#     teachers = user.objects.filter(role='teacher')
#     admins = user.objects.filter(role='admin')

#     context = {

#         "users_teacher": user.objects.filter(role='teacher'),
#         "users_student": students_with_flag,  # pass with flag
#         "users_admin": user.objects.filter(role='admin'),
        
#         # "users_teacher": teachers,
#         # "users_student": students,
#         # "users_admin": admins,
#         "classes": assigned_classes,
#         "subjects": assigned_subjects,
#         "syllabi": syllabi,
#         "timetables": timetables,
#         "tab": tab,
#         'role': logged_in_user.role,# Pass role for sidebar
#     }

#     return render(request, "TeacherPages/teacher.html", context)

# from django.utils import timezone
# import json

# def teacher_view(request):
#     if "user_id" not in request.session:
#         return redirect('login')
#     logged_in_user = user.objects.get(id=request.session["user_id"])
#     if logged_in_user.role != "teacher":
#         return redirect('login')
    
#     tab = request.GET.get("tab", "dashboard")
    
#     # Subjects assigned to this teacher
#     assigned_subjects = AssignSubject.objects.filter(teacher=logged_in_user)
    
#     # Classes where teacher teaches subjects
#     assigned_classes = ClassRoom.objects.filter(
#         id__in=assigned_subjects.values_list('assigned_class', flat=True)
#     )
    
#     # Students by class
#     students_by_class = {}
#     for cls in assigned_classes:
#         students_qs = user.objects.filter(role='student', class_name=cls)
#         students_by_class[cls.id] = [
#             {"id": s.id, "name": s.name, "roll_no": s.admission_no}
#             for s in students_qs
#         ]
    
#     # Subjects JSON for JS
#     subjects_json = [
#         {"id": sub.id, "name": sub.subject.subject_name, "class_id": sub.assigned_class.id, "teacher_id": sub.teacher.id if sub.teacher else None}
#         for sub in assigned_subjects
#     ]
    
#     context = {
#         "classes": assigned_classes,
#         "students_by_class": json.dumps(students_by_class),
#         "subjects_json": json.dumps(subjects_json),
#         "today": timezone.now().date(),
#         "tab": tab,
#         "role": logged_in_user.role,
#     }
    
#     return render(request, "TeacherPages/teacher_attendance.html", context)
 
# def teacher_view_students(request):
#     teacher = request.user  # logged-in teacher
    
#     students_list = []

#     # 1️⃣ CLASS TEACHER → Get all students of their class
#     if hasattr(teacher, "class_teacher_for") and teacher.class_teacher_for:
#         class_students = Student.objects.filter(class_name=teacher.class_teacher_for)
#         for s in class_students:
#             students_list.append({
#                 "student": s,
#                 "is_class_student": True   # highlight
#             })

#     # 2️⃣ SUBJECT TEACHER → Get students of classes they teach
#     if hasattr(teacher, "subjects_assigned"):
#         subject_classes = teacher.subjects_assigned.values_list("class_name", flat=True)

#         subject_students = Student.objects.filter(class_name__in=subject_classes)

#         for s in subject_students:
#             # avoid duplicate students already added above
#             if not any(item["student"].id == s.id for item in students_list):
#                 students_list.append({
#                     "student": s,
#                     "is_class_student": False
#                 })

#     context = {
#         "users_student": students_list,
#     }
#     return render(request, "teacher/teacher_students.html", context)

def teacher_view_students(request):
    logged_user = user.objects.get(id=request.session.get("user_id"))

    if logged_user.role != "teacher":
        return redirect("login")

    # FILTER PARAMETER
    filter_class = request.GET.get("class")

    # 1️⃣ CLASS TEACHER CLASS
    class_teacher_class = ClassRoom.objects.filter(class_teacher=logged_user).first()

    # 2️⃣ SUBJECT TEACHER CLASSES
    subject_class_ids = AssignSubject.objects.filter(
        teacher=logged_user
    ).values_list("assigned_class", flat=True)

    # COMBINE BOTH FOR FILTER DROPDOWN
    all_classes = ClassRoom.objects.filter(
        Q(id__in=subject_class_ids) | Q(id=class_teacher_class.id if class_teacher_class else None)
    ).distinct()

    # ⭐ CLASS TEACHER STUDENTS
    class_teacher_students = []
    if class_teacher_class:
        class_teacher_students = user.objects.filter(
            role="student",
            class_name=class_teacher_class
        )

    # ⭐ SUBJECT TEACHER STUDENTS
    subject_teacher_students = user.objects.filter(
        role="student",
        class_name_id__in=subject_class_ids
    )

    # REMOVE class-teacher duplicates
    if class_teacher_class:
        subject_teacher_students = subject_teacher_students.exclude(
            class_name=class_teacher_class
        )

    # ⭐ APPLY FILTER
    if filter_class:
        class_teacher_students = class_teacher_students.filter(class_name_id=filter_class)
        subject_teacher_students = subject_teacher_students.filter(class_name_id=filter_class)

    return render(request, "TeacherPages/view_students.html", {
        "class_teacher_students": class_teacher_students,
        "subject_teacher_students": subject_teacher_students,
        "class_teacher_class": class_teacher_class,
        "all_classes": all_classes,
        "filter_class": filter_class,
    })

def student_profile_view(request, student_id):
    try:
        student = user.objects.get(id=student_id, role='student')
    except user.DoesNotExist:
        return redirect('teacher')  # fallback, or you can show 404

    context = {
        'student': student
    }
    return render(request, "StudentPages/student_profile.html", context)


@login_required
def mark_attendance(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        date = request.POST.get("date")

        students = user.objects.filter(role="student" ,assigned_class_id=class_id)

        context = {
            "students": students,
            "class_id": class_id,
            "date": date,
        }
        return render(request, "mark_attendance.html", context)

    return redirect("teacher_dashboard")

@login_required
def submit_attendance(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        date = request.POST.get("date")

        for key, value in request.POST.items():
            if key.startswith("student_"):
                student_id = key.split("_")[1]
                status = value

                Attendance.objects.create(
                    student_id=student_id,
                    date=date,
                    status=status,
                )

        messages.success(request, "Attendance submitted successfully.")
        return redirect("teacher_dashboard")

    return redirect("teacher_dashboard")

@login_required
def add_marks(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        exam_name = request.POST.get("exam_name")

        subject_obj = AssignSubject.objects.get(id=subject_id)

        students = user.objects.filter(
            role="student",
            assigned_class=subject_obj.assigned_class
        )

        context = {
            "students": students,
            "exam_name": exam_name,
            "subject_id": subject_id,
        }
        return render(request, "add_marks.html", context)

    return redirect("teacher_dashboard")

@login_required
def submit_marks(request):
    if request.method == "POST":
        exam_name = request.POST.get("exam_name")
        subject_id = request.POST.get("subject_id")

        for key, value in request.POST.items():
            if key.startswith("student_"):
                student_id = key.split("_")[1]
                mark = value

                Marks.objects.create(
                    student_id=student_id,
                    subject_id=subject_id,
                    exam_name=exam_name,
                    marks=mark,
                )

        messages.success(request, "Marks added successfully.")
        return redirect("teacher_dashboard")

    return redirect("teacher_dashboard")

@login_required
def send_notification(request):
    if request.method == "POST":
        message = request.POST.get("message")

        Notification.objects.create(
            sender=request.user,
            receiver_role="admin",
            message=message,
        )

        messages.success(request, "Notification sent to Admin.")
        return redirect("teacher_dashboard")

    return HttpResponse("Invalid request")


 
