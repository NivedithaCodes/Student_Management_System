from django.urls import path
from .views import home_view,login_view,signup_view,student_view


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
    # path('student/', student_view, name='student'),
    
    # Redirect pages after login
    path('student/', views.student_home, name='student'),
    path('parent/', views.parent_home, name='parent'),
    path('teacher/', views.teacher_home, name='teacher'),
    path('principal/', views.principal_home, name='principal'),
]



