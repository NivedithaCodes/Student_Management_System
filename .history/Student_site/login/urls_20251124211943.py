from django.urls import path
from .views import home_view,login_view,signup_view,student_view


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
    path('student/', student_view, name='student'),
    path('student/dashboard/',student_dashboard, name='student_dashboard'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('principal/dashboard/', views.principal_dashboard, name='principal_dashboard'),
]

