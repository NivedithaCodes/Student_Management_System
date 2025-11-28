from django.shortcuts import render,redirect
from login.models import Student,user
from django.contrib import messages

# Create your views here.
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        dept = request.POST['department']

        Student.objects.create(name=name,email=email,age=age,department=dept)
        return redirect('view_students')
    
    return render(request,'add_student.html')

def home_view(request):
    return render(request,'home.html')

def signup_view(request,popup=None):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # check if user exists
        if user.objects.filter(email=email).exists():
            return render(request, 'home.html', {
                'popup': 'signup',
                'error_text': 'User already exists!'
            })

        # create user
        user.objects.create(name=name, email=email, password=password)
        messages.success(request, "Signup Successful")
        return redirect('student')

    return render(request, 'home.html')

def login_view(request,popup=None):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user exists in DB
        try:
            user_obj = user.objects.get(email=email)
            if user_obj.password == password:
                # Login success
                messages.success(request, f"Login Successfully")
                return redirect('student')  # replace with your homepage
            else:
                #  Wrong password
                messages.success(request, f"Incorrect Password")
                return render(request, 'home.html')
        except user.DoesNotExist:
            #  No user found
            messages.success(request, f"User Not Found")
            return render(request, 'home.html')
    return render(request, 'index.html')
    
 
# def admin_view_view(request):
#     return render(request,'admin.html')

 










