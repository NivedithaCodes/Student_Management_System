from django.shortcuts import render

# Create your views here.
def add_student(request):
    if request.method == 'POST':
        name = request.POST['NAE']
def home_view(request):
    return render(request,'home.html')