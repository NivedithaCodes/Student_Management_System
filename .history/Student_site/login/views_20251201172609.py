# # from django.shortcuts import render,redirect
# # from login.models import user
# # from django.contrib import messages

# # def home_view(request):
# #     return render(request,'home.html')

# # def signup_view(request,popup=None):
# #     if request.method == 'POST':
# #         name = request.POST.get("name")
# #         email = request.POST.get("email")
# #         password = request.POST.get("password")

# #         admission_no=request.POST.get("admission_no")
# #         dob=request.POST.get("dob")
# #         mobile=request.POST.get("mobile")

# #         confirm_password = request.POST.get("confirm_password")
# #         role = request.POST.get("role")
        
# #         if user.objects.filter(email=email).exists():
# #             return render(request, 'home.html', {
# #                 'popup': 'signup',
# #                 'signup_error': 'User already exists!'
# #             })
        
# #         # SAVE USER with ROLE
# #         user.objects.create(
# #             admission_no=admission_no,
# #             name=name,
# #             email=email,
# #             dob=dob,
# #             mobile=mobile,
# #             password=password,
# #             role=role
# #         )

# #         # create user
# #         messages.success(request, "Signup Successful")
# #         return redirect('login')

# #     return render(request, 'home.html')

# # def login_view(request, popup=None):
# #     if request.method == "POST":
# #         email = request.POST.get("email")
# #         password = request.POST.get("password")

# #         # Check if user exists in DB
# #         try:
# #             user_obj = user.objects.get(email=email)

# #             if user_obj.password == password:
# #                 # Login success
# #                 messages.success(request, "Login Successfully")

# #                 # ⭐ ROLE-BASED REDIRECTION ADDED HERE  
# #                 if user_obj.role == "student":
# #                     return redirect('student')
# #                 elif user_obj.role == "parent":
# #                     return redirect('parent')
# #                 elif user_obj.role == "teacher":
# #                     return redirect('teacher')
# #                 elif user_obj.role == "principal":
# #                     return redirect('principal')
# #                 else:
# #                     return redirect('student')  # default

# #             else:
# #                 # Incorrect password
# #                 return render(request, 'home.html',
# #                                {'popup': 'login',
# #                                  "login_error": "Incorrect Password"
# #                                  })

# #         except user.DoesNotExist:
# #             # User not found
# #             return render(request, 'home.html',
# #                            {'popup': 'login',
# #                             "login_error": "User Not Found"
# #                             })

# #     return render(request, 'home.html')

 
# # # def student_view(request):
# # #     return render(request,'student.html')

# # def home_view(request):
# #     return render(request, "home.html")


# # def student_view(request):
# #     return render(request, "student.html")


# # def parent_view(request):
# #     return render(request, "parent.html")


# # def teacher_view(request):
# #     return render(request, "teacher.html")


# # def principal_view(request):
# #     return render(request, "principal.html")

# # def logout_view(request):
# #     request.session.flush()   # clears login session
# #     return redirect('home')   # redirect to home or login page

 
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from .models import user

# # ---------- existing auth / pages ----------
# def home_view(request):
#     return render(request, "home.html")

# def signup_view(request, popup=None):
#     if request.method == 'POST':
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         admission_no = request.POST.get("admission_no")
#         dob = request.POST.get("dob")
#         mobile = request.POST.get("mobile")

#         confirm_password = request.POST.get("confirm_password")
#         role = request.POST.get("role")

#         if user.objects.filter(email=email).exists():
#             return render(request, 'home.html', {
#                 'popup': 'signup',
#                 'signup_error': 'User already exists!'
#             })

#         user.objects.create(
#             admission_no=admission_no,
#             name=name,
#             email=email,
#             dob=dob or None,
#             mobile=mobile,
#             password=password,
#             role=role
#         )

#         messages.success(request, "Signup Successful")
#         return redirect('login')

#     return render(request, 'home.html')

# def login_view(request, popup=None):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user_obj = user.objects.get(email=email)
#             if user_obj.password == password:
#                 messages.success(request, "Login Successfully")
#                 if user_obj.role == "student":
#                     return redirect('student')
#                 elif user_obj.role == "parent":
#                     return redirect('parent')
#                 elif user_obj.role == "teacher":
#                     return redirect('teacher')
#                 elif user_obj.role == "principal":
#                     return redirect('principal')
#                 elif user_obj.role == "admin":
#                     return redirect('principal')  # admins use principal page
#                 else:
#                     return redirect('student')
#             else:
#                 return render(request, 'home.html', {'popup': 'login', "login_error": "Incorrect Password"})
#         except user.DoesNotExist:
#             return render(request, 'home.html', {'popup': 'login', "login_error": "User Not Found"})

#     return render(request, 'home.html')


# def student_view(request):
#     return render(request, "student.html")

# def parent_view(request):
#     return render(request, "parent.html")

# def teacher_view(request):
#     return render(request, "teacher.html")

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

# def logout_view(request):
#     request.session.flush()
#     return redirect('home')


# # ---------- CRUD actions for admin dashboard ----------
# def add_admin(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # basic duplicate email protection
#         if user.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect('principal')

#         user.objects.create(
#             name=name,
#             email=email,
#             password=password,
#             role="admin"
#         )
#     return redirect('principal')

# def add_teacher(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         subject = request.POST.get("subject")

#         if user.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect('principal')

#         user.objects.create(
#             name=name,
#             email=email,
#             password="teacher@123",   # default password; you can change to posted password if you add it in the form
#             role="teacher",
#             subject=subject
#         )
#     return redirect('principal')

# def add_student(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         class_name = request.POST.get("class")

#         if user.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect('principal')

#         user.objects.create(
#             name=name,
#             email=email,
#             password="student@123",
#             role="student",
#             class_name=class_name
#         )
#     return redirect('principal')

# def edit_user(request, id):
#     u = get_object_or_404(user, id=id)

#     if request.method == "POST":
#         u.name = request.POST.get("name")
#         u.email = request.POST.get("email")
#         # if password field present, update it
#         pwd = request.POST.get("password")
#         if pwd:
#             u.password = pwd

#         # role-specific fields
#         if u.role == "teacher":
#             u.subject = request.POST.get("subject")
#         if u.role == "student":
#             u.class_name = request.POST.get("class")

#         u.save()
#         return redirect('principal')

#     # GET -> render small edit page
#     return render(request, "edit_user.html", {"user": u})

# def delete_user(request, id):
#     u = get_object_or_404(user, id=id)
#     u.delete()
#     return redirect('principal')




