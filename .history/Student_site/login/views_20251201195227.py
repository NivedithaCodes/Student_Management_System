from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import user,ClassRoom,Subject,AssignSubject,Syllabus,Timetable

# ---------- existing auth / pages ----------
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
            if user_obj.password == password:
                messages.success(request, "Login Successfully")
                if user_obj.role == "student":
                    return redirect('student')
                elif user_obj.role == "parent":
                    return redirect('parent')
                elif user_obj.role == "teacher":
                    return redirect('teacher')
                elif user_obj.role == "principal":
                    return redirect('principal')
                elif user_obj.role == "admin":
                    return redirect('principal')  # admins use principal page
                else:
                    return redirect('student')
            else:
                return render(request, 'home.html', {'popup': 'login', "login_error": "Incorrect Password"})
        except user.DoesNotExist:
            return render(request, 'home.html', {'popup': 'login', "login_error": "User Not Found"})

    return render(request, 'home.html')


def student_view(request):
    return render(request, "student.html")

def parent_view(request):
    return render(request, "parent.html")

def teacher_view(request):
    return render(request, "teacher.html")

# def principal_view(request):
#     # Render principal.html with admin/teacher/student lists
#     users_admin = user.objects.filter(role="admin")
#     users_teacher = user.objects.filter(role="teacher")
#     users_student = user.objects.filter(role="student")
#     return render(request, "principal.html", {
#         "users_admin": users_admin,
#         "users_teacher": users_teacher,
#         "users_student": users_student
#     })

def logout_view(request):
    request.session.flush()
    return redirect('home')


# ---------- CRUD actions for admin dashboard ----------
def add_admin(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # basic duplicate email protection
        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('principal')

        user.objects.create(
            name=name,
            email=email,
            password=password,
            role="admin"
        )
    return redirect('principal')

def add_teacher(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")

        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('principal')

        user.objects.create(
            name=name,
            email=email,
            password="teacher@123",   # default password; you can change to posted password if you add it in the form
            role="teacher",
            subject=subject
        )
    return redirect('principal')

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        class_name = request.POST.get("class")

        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('principal')

        user.objects.create(
            name=name,
            email=email,
            password="student@123",
            role="student",
            class_name=class_name
        )
    return redirect('principal')

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
        if u.role == "student":
            u.class_name = request.POST.get("class")

        u.save()
        return redirect('principal')

    # GET -> render small edit page
    return render(request, "edit_user.html", {"user": u})

def delete_user(request, id):
    u = get_object_or_404(user, id=id)
    u.delete()
    return redirect('principal')

# def principal_view(request):
#     users_admin = user.objects.filter(role='admin')
#     users_teacher = user.objects.filter(role='teacher')
#     users_student = user.objects.filter(role='student')
#     classes = ClassRoom.objects.all()
#     subjects = Subject.objects.all()

#     return render(request, 'principal.html', {
#         'users_admin': users_admin,
#         'users_teacher': users_teacher,
#         'users_student': users_student,
#         'classes': classes,
#         'subjects': subjects
#     })

 
# ------------------------------
# NEW: CRUD CLASS
# ------------------------------
# def add_class(request):
#     if request.method == "POST":
#         class_name = request.POST['class_name']
#         section = request.POST['section']
#         ClassRoom.objects.create(class_name=class_name, section=section)
#     return redirect('principal')

# def edit_class(request, id):
#     cls = get_object_or_404(ClassRoom, id=id)
#     if request.method == "POST":
#         cls.class_name = request.POST['class_name']
#         cls.section = request.POST['section']
#         teacher_id = request.POST.get('class_teacher')
#         if teacher_id:
#             cls.class_teacher = user.objects.get(id=teacher_id)
#         cls.save()
#         return redirect('principal')
#     teachers = user.objects.filter(role='teacher')
#     return render(request, 'edit_class.html', {'class': cls, 'teachers': teachers})

# def delete_class(request, id):
#     cls = get_object_or_404(ClassRoom, id=id)
#     cls.delete()
#     return redirect('principal')

# # ------------------------------
# # NEW: CRUD SUBJECT
# # ------------------------------
# def add_subject(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         class_id = request.POST['class_id']
#         teacher_id = request.POST.get('teacher_id')
#         cls = ClassRoom.objects.get(id=class_id)
#         teacher = user.objects.get(id=teacher_id) if teacher_id else None
#         Subject.objects.create(name=name, class_room=cls, teacher=teacher)
#     return redirect('principal')

# def edit_subject(request, id):
#     sub = get_object_or_404(Subject, id=id)
#     if request.method == "POST":
#         sub.name = request.POST['name']
#         class_id = request.POST.get('class_id')
#         teacher_id = request.POST.get('teacher_id')
#         if class_id:
#             sub.class_room = ClassRoom.objects.get(id=class_id)
#         if teacher_id:
#             sub.teacher = user.objects.get(id=teacher_id)
#         sub.save()
#         return redirect('principal')
#     classes = ClassRoom.objects.all()
#     teachers = user.objects.filter(role='teacher')
#     return render(request, 'edit_subject.html', {'subject': sub, 'classes': classes, 'teachers': teachers})

# def delete_subject(request, id):
#     sub = get_object_or_404(Subject, id=id)
#     sub.delete()
#     return redirect('principal')

# # ------------------------------
# # NEW: CHANGE PASSWORD
# # ------------------------------
# def change_password(request, id):
#     u = get_object_or_404(user, id=id)
#     if request.method == "POST":
#         new_password = request.POST['new_password']
#         confirm_password = request.POST['confirm_password']
#         if new_password == confirm_password:
#             u.password = new_password
#             u.save()
#             messages.success(request, "Password changed successfully!")
#         else:
#             messages.error(request, "Passwords do not match!")
#         return redirect('principal')
#     return render(request, 'change_password.html', {'user': u})

# # ------------------------------
# # NEW: ASSIGN TEACHER
# # ------------------------------
# def assign_teacher(request):
#     if request.method == "POST":
#         teacher_id = request.POST.get('teacher_id')
#         class_id = request.POST.get('class_id')
#         subject_id = request.POST.get('subject_id')

#         cls = get_object_or_404(ClassRoom, id=class_id)
#         teacher = get_object_or_404(user, id=teacher_id)

#         # assign teacher to class
#         cls.class_teacher = teacher
#         cls.save()

#         # assign teacher to subject
#         if subject_id:
#             sub = get_object_or_404(Subject, id=subject_id)
#             sub.teacher = teacher
#             sub.save()

#     return redirect('principal')

 

# # --------------------------------------
# # DASHBOARD / PRINCIPAL PAGE
# # --------------------------------------
def principal_dashboard(request):
    context = {
        "users_admin": user.objects.filter(role="admin"),
        "users_teacher": user.objects.filter(role="teacher"),
        "users_student": user.objects.filter(role="student"),
        "classes": ClassRoom.objects.all(),
        "subjects": Subject.objects.all(),
        "syllabus_list": Syllabus.objects.all(),
        "timetables": Timetable.objects.all(),
    }
    return render(request, "principal.html", context)

# # --------------------------------------
# # EDIT / DELETE USER
# # --------------------------------------
# def edit_user(request, id):
#     u = get_object_or_404(user, id=id)
#     if request.method == "POST":
#         u.name = request.POST.get("name")
#         u.email = request.POST.get("email")
#         u.subject = request.POST.get("subject", u.subject)
#         u.class_name = request.POST.get("class_name", u.class_name)
#         u.save()
#         return redirect("principal_dashboard")
#     return render(request, "edit_user.html", {"user": u})


# def delete_user(request, id):
#     u = get_object_or_404(user, id=id)
#     u.delete()
#     return redirect("principal_dashboard")


# --------------------------------------
# CLASS MANAGEMENT
# --------------------------------------
def add_class(request):
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        ClassRoom.objects.create(class_name=class_name)
    return redirect("principal_d")


def edit_class(request, id):
    cls = get_object_or_404(ClassRoom, id=id)
    if request.method == "POST":
        cls.class_name = request.POST.get("class_name")
        cls.section = request.POST.get("section", cls.section)
        cls.save()
        return redirect("principal")
    return render(request, "edit_class.html", {"class": cls})


def delete_class(request, id):
    cls = get_object_or_404(ClassRoom, id=id)
    cls.delete()
    return redirect("principal")

# SUBJECT MANAGEMENT
 
def add_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        assigned_class_id = request.POST.get("assigned_class")
        teacher_id = request.POST.get("teacher")
        assigned_class = ClassRoom.objects.get(id=assigned_class_id)
        teacher_obj = user.objects.get(id=teacher_id) if teacher_id else None
        Subject.objects.create(
            subject_name=subject_name,
            assigned_class=assigned_class,
            teacher=teacher_obj,
        )
    return redirect("principal")


def edit_subject(request, id):
    sub = get_object_or_404(Subject, id=id)
    if request.method == "POST":
        sub.subject_name = request.POST.get("subject_name")
        class_id = request.POST.get("assigned_class")
        teacher_id = request.POST.get("teacher")
        sub.assigned_class = ClassRoom.objects.get(id=class_id)
        sub.teacher = user.objects.get(id=teacher_id) if teacher_id else None
        sub.save()
        return redirect("principal")
    context = {
        "subject": sub,
        "classes": ClassRoom.objects.all(),
        "users_teacher": user.objects.filter(role="teacher"),
    }
    return render(request, "edit_subject.html", context)


def delete_subject(request, id):
    sub = get_object_or_404(Subject, id=id)
    sub.delete()
    return redirect("principal")


# SYLLABUS MANAGEMENT
 
# def add_syllabus(request):
#     if request.method == "POST":
#         class_id = request.POST.get("class_room")
#         subject_id = request.POST.get("subject")
#         file = request.FILES.get("syllabus_file")
#         class_obj = ClassRoom.objects.get(id=class_id)
#         subject_obj = Subject.objects.get(id=subject_id)
#         Syllabus.objects.create(class_room=class_obj, subject=subject_obj, syllabus_file=file)
#     return redirect("principal_dashboard")


# def edit_syllabus(request, id):
#     syl = get_object_or_404(Syllabus, id=id)
#     if request.method == "POST":
#         syl.class_room = ClassRoom.objects.get(id=request.POST.get("class_room"))
#         syl.subject = Subject.objects.get(id=request.POST.get("subject"))
#         if request.FILES.get("syllabus_file"):
#             syl.syllabus_file = request.FILES.get("syllabus_file")
#         syl.save()
#         return redirect("principal_dashboard")
#     context = {
#         "syllabus": syl,
#         "classes": ClassRoom.objects.all(),
#         "subjects": Subject.objects.all(),
#     }
#     return render(request, "edit_syllabus.html", context)


# def delete_syllabus(request, id):
#     syl = get_object_or_404(Syllabus, id=id)
#     syl.delete()
#     return redirect("principal_dashboard")
def add_syllabus(request):
    if request.method == "POST":
        class_room_id = request.POST.get("class_room")
        subject_id = request.POST.get("subject")
        syllabus_file = request.FILES.get("syllabus_file")

        class_room = ClassRoom.objects.get(id=class_room_id)
        subject = Subject.objects.get(id=subject_id)

        Syllabus.objects.create(
            class_room=class_room,
            subject=subject,
            syllabus_file=syllabus_file
        )
        return redirect("principal")

    return redirect("principal")


def edit_syllabus(request, id):
    syllabus = Syllabus.objects.get(id=id)

    if request.method == "POST":
        syllabus.class_room_id = request.POST.get("class_room")
        syllabus.subject_id = request.POST.get("subject")

        if request.FILES.get("syllabus_file"):
            syllabus.syllabus_file = request.FILES.get("syllabus_file")

        syllabus.save()
        return redirect("principal")

    return redirect("principal")


def delete_syllabus(request, id):
    syllabus = Syllabus.objects.get(id=id)
    syllabus.delete()
    return redirect("principal")


# # --------------------------------------
# # TIMETABLE MANAGEMENT
# # --------------------------------------
# def add_timetable(request):
#     if request.method == "POST":
#         class_id = request.POST.get("class_room")
#         file = request.FILES.get("timetable_file")
#         class_obj = ClassRoom.objects.get(id=class_id)
#         Timetable.objects.create(class_room=class_obj, timetable_file=file)
#     return redirect("principal_dashboard")


# def edit_timetable(request, id):
#     tt = get_object_or_404(Timetable, id=id)
#     if request.method == "POST":
#         tt.class_room = ClassRoom.objects.get(id=request.POST.get("class_room"))
#         if request.FILES.get("timetable_file"):
#             tt.timetable_file = request.FILES.get("timetable_file")
#         tt.save()
#         return redirect("principal_dashboard")
#     context = {
#         "timetable": tt,
#         "classes": ClassRoom.objects.all(),
#     }
#     return render(request, "edit_timetable.html", context)


# def delete_timetable(request, id):
#     tt = get_object_or_404(Timetable, id=id)
#     tt.delete()
#     return redirect("principal_dashboard")
