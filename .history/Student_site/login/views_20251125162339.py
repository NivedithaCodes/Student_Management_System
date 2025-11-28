from django.shortcuts import render,redirect
from login.models import user
from django.contrib import messages

def home_view(request):
    return render(request,'home.html')

def signup_view(request,popup=None):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        admission_no=request.POST.get("admission_no")
        dob=request.POST.get("dob")
        mobile=request.POST.get("mobile")

        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        
         # 1. Password mismatch
        if password != confirm_password:
            return render(request, "signup.html", {
                "signup_error": "Passwords do not match!"
            })

        # 2.check if user exists
        if user.objects.filter(email=email).exists():
            return render(request, 'home.html', {
                'popup': 'signup',
                'signuerror': 'User already exists!'
            })
        
        # SAVE USER with ROLE
        user.objects.create(
            admission_no=admission_no,
            name=name,
            email=email,
            dob=dob,
            mobile=mobile,
            password=password,
            role=role
        )

        # create user
        user.objects.create(name=name, email=email, password=password,role=role)
        messages.success(request, "Signup Successful")
        return redirect('login')

    return render(request, 'home.html')

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
                # messages.success(request, "Incorrect Password")
                return render(request, 'home.html',
                               {'popup': 'login',
                                 "login_error": "Incorrect Password"
                                 })

        except user.DoesNotExist:
            # User not found
            # messages.success(request, "User Not Found")
            return render(request, 'home.html',
                           {'popup': 'login',
                            "login_error": "User Not Found"
                            })

    return render(request, 'home.html')

 
# def student_view(request):
#     return render(request,'student.html')

def home_view(request):
    return render(request, "home.html")


def student_view(request):
    return render(request, "student.html")


def parent_view(request):
    return render(request, "parent.html")


def teacher_view(request):
    return render(request, "teacher.html")


def principal_view(request):
    return render(request, "principal.html")











