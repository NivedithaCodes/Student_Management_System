from django.shortcuts import render,redirect
from login.models import user
from django.contrib import messages

# Create your views here.
# def add_student(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         age = request.POST['age']
#         dept = request.POST['department']

#         Student.objects.create(name=name,email=email,age=age,department=dept)
#         return redirect('view_students')
    
#     return render(request,'add_student.html')

def home_view(request):
    return render(request,'home.html')

def signup_view(request,popup=None):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        # check if user exists
        if user.objects.filter(email=email).exists():
            return render(request, 'home.html', {
                'popup': 'signup',
                'error_text': 'User already exists!'
            })
        
        # SAVE USER with ROLE
        user.objects.create(
           name=name,
           email=email,
           password=password,
           role=role
        )

        # create user
        user.objects.create(name=name, email=email, password=password,role=role)
        messages.success(request, "Signup Successful")
        return redirect('login')

    return render(request, 'home.html')

# def login_view(request,popup=None):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Check if user exists in DB
#         try:
#             user_obj = user.objects.get(email=email)
#             if user_obj.password == password:
#                 # Login success
#                 messages.success(request, f"Login Successfully")
#                 return redirect('student')  # replace with your homepage
#             else:
#                 #  Wrong password
#                 messages.success(request, f"Incorrect Password")
#                 return render(request, 'home.html')
#         except user.DoesNotExist:
#             #  No user found
#             messages.success(request, f"User Not Found")
#             return render(request, 'home.html')
#     return render(request, 'home.html')

# def login_view(request, popup=None):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user_obj = user.objects.get(email=email)

#             if user_obj.password == password:

#                 # redirect based on role
#                 if user_obj.role == "student":
#                     return redirect('student_dashboard')

#                 elif user_obj.role == "parent":
#                     return redirect('parent_dashboard')

#                 elif user_obj.role == "teacher":
#                     return redirect('teacher_dashboard')

#                 elif user_obj.role == "principal":
#                     return redirect('principal_dashboard')

#                 else:
#                     return redirect('student_dashboard')

#             else:
#                 return render(request, 'home.html', {
#                     'popup': 'login',
#                     'login_error': 'Incorrect Password'
#                 })

#         except user.DoesNotExist:
#             #  No user found
#             return render(request, 'home.html', {
#                 'popup': 'login',
#                 'login_error': 'User Not Found'
#             })

#     return render(request, 'home.html')

def login_view(request, popup=None):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user exists in DB
        try:
            user_obj = user.objects.get(email=email)

            if user_obj.password == password:
                # Login success
                messages.success(request, "Login Successfully")

                # ⭐ ROLE-BASED REDIRECTION ADDED HERE  
                if user_obj.role == "student":
                    return redirect('student')
                elif user_obj.role == "parent":
                    return redirect('parent')
                elif user_obj.role == "teacher":
                    return redirect('teacher')
                elif user_obj.role == "principal":
                    return redirect('principal')
                else:
                    return redirect('student')  # default

            else:
                # Incorrect password
                messages.success(request, "Incorrect Password")
                return render(request, 'home.html',
                               {'popup': 'login',
                                 "login_error": "Incorrect Password"
                                 })

        except user.DoesNotExist:
            # User not found
            messages.success(request, "User Not Found")
            return render(request, 'home.html',
                           {'popup': 'login',
                            "login_error": "User Not Found"
                            })

    return render(request, 'home.html')

 
# def student_view(request):
#     return render(request,'student.html')

 def home_view(request):
    return render(request, "home.html")


def student_home(request):
    return render(request, "student_home.html")


def parent_home(request):
    return render(request, "parent_home.html")


def teacher_home(request):
    return render(request, "teacher_home.html")


def principal_home(request):
    return render(request, "principal_home.html")











