from django.shortcuts import render,redirect
from login.models import Student

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









