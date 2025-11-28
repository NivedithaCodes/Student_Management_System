from django.urls import path
from .views import home_view,login_view,signup_view,student_view,pa


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
    # path('student/', student_view, name='student'),
    
    # Redirect pages after login
    path('student/', student_view, name='student'),
    path('parent/', parent_view, name='parent'),
    path('teacher/', teacher_view, name='teacher'),
    path('principal/',principal_view, name='principal'),
]



