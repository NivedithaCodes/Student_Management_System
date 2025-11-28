from django.shortcuts import render

# Create your views here.
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.
def home_view(request):
    return render(request,'home.html')