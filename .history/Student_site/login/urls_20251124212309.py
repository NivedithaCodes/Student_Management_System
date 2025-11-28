from django.urls import path
from .views import home_view,login_view,signup_view,student_view


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
    path('student/', student_view, name='student'),
    path('student/dashboard/',student, name='student_dashboard'),
    path('parent/dashboard/', , name='parent_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('principal/dashboard/', views.principal_dashboard, name='principal_dashboard'),
    from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    # Signup & Login
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),

    # Redirect pages after login
    path('student/', views.student_home, name='student'),
    path('parent/', views.parent_home, name='parent'),
    path('teacher/', views.teacher_home, name='teacher'),
    path('principal/', views.principal_home, name='principal'),
]

]

