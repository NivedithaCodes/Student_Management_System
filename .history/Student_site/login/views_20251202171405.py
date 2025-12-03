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
            return redirect('/principal/?tab=admin')

        user.objects.create(
            name=name,
            email=email,
            password=password,
            role="admin"
        )
    return redirect('/principal/?tab=admin') # redirect only after POST
    
    # GET request → show form
    # return render(request, "add_admin.html")


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
        class_name = request.POST.get("class")

        if user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/principal/?tab=student')

        user.objects.create(
            name=name,
            email=email,
            password="student@123",
            role="student",
            class_name=class_name
        )
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

        # u.save()
        # return redirect('add_admin')

    # GET -> render small edit page
    return render(request, "edit_user.html", {"user": u})

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

# DASHBOARD / PRINCIPAL PAGE
def principal_view(request):
    tab = request.GET.get("tab", "dashboard")
    context = {
        "tab": tab,
        "users_admin": user.objects.filter(role="admin"),
        "users_teacher": user.objects.filter(role="teacher"),
        "users_student": user.objects.filter(role="student"),
        "classes": ClassRoom.objects.all(),
        "subjects": Subject.objects.all(),
        "syllabi": Syllabus.objects.all(),
        "timetables": Timetable.objects.all(),

    }
    return render(request, "principal.html", context)

# CLASS MANAGEMENT
 
def add_class(request):
    teachers = user.objects.filter(role='teacher')
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        section = request.POST.get("section") or None  
        max_strength = request.POST.get('max_strength') or None
        teacher_id = request.POST.get("class_teacher") or None
        class_teacher = user.objects.get(id=teacher_id) if teacher_id else None
        ClassRoom.objects.create(class_name=class_name, section=section,max_strength=max_strength,class_teacher=)
        return redirect("/principal/?tab=class") 
    return redirect("/principal/?tab=class") 
    
def edit_class(request, id):
    cls = get_object_or_404(ClassRoom, id=id)
    teachers = user.objects.filter(role="teacher")

    if request.method == "POST":
        cls.class_name = request.POST.get("class_name")
        cls.section = request.POST.get("section") or None
        cls.max_strength = request.POST.get("max_strength") or None

        # update class_teacher 
        teacher_id = request.POST.get("class_teacher")
        if teacher_id:
            try:
                cls.class_teacher = user.objects.get(id=cls.teacher_id)
            except user.DoesNotExist:
                cls.class_teacher = None
        else:
            cls.class_teacher = None

        cls.save()
        return redirect("/principal/?tab=class")   

    return render(request, "edit_class.html", {"cls": cls, "teachers": teachers})


def delete_class(request, id):
    cls = get_object_or_404(ClassRoom, id=id)
    cls.delete()
    return redirect("/principal/?tab=class")  


# SUBJECT MANAGEMENT
def add_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        assigned_class_id = request.POST.get("assigned_class")
        teacher_id = request.POST.get("teacher")

        # basic validation
        if not subject_name or not assigned_class_id:
            messages.error(request, "Subject name and class are required.")
            return redirect("/principal/?tab=subject")

        assigned_class = ClassRoom.objects.get(id=assigned_class_id)
        teacher_obj = user.objects.get(id=teacher_id) if teacher_id else None

        Subject.objects.create(
            subject_name=subject_name,
            assigned_class=assigned_class,
            teacher=teacher_obj,
        )
    return redirect("/principal/?tab=subject")


def edit_subject(request, id):
    sub = get_object_or_404(Subject, id=id)
    if request.method == "POST":
        sub.subject_name = request.POST.get("subject_name")
        class_id = request.POST.get("assigned_class")
        teacher_id = request.POST.get("teacher")
        if class_id:
            sub.assigned_class = ClassRoom.objects.get(id=class_id)
        sub.teacher = user.objects.get(id=teacher_id) if teacher_id else None
        sub.save()
        return redirect("/principal/?tab=subject") 
    context = {
        "subject": sub,
        "classes": ClassRoom.objects.all(),
        "users_teacher": user.objects.filter(role="teacher"),
    }
    return render(request, "edit_subject.html", context)


def delete_subject(request, id):
    sub = get_object_or_404(Subject, id=id)
    sub.delete()
    return redirect("/principal/?tab=subject") 


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
        return redirect("/principal/?tab=syllabus")

    context = {
        "syllabus": syllabus,
        "classes": ClassRoom.objects.all(),
        "subjects": Subject.objects.all(),
    }
    return render(request, "edit_syllabus.html", context)


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
    return render(request, "edit_timetable.html", context)

def delete_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    timetable.delete()
    return redirect("/principal/?tab=timetable")


 
