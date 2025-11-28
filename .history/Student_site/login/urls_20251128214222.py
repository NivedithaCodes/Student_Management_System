# from django.urls import path
# from .views import home_view,login_view,signup_view,student_view,parent_view,teacher_view,principal_view,logout_view,add_admin,add_student,add_teacher,edit_user,delete_user


# urlpatterns = [
#     path('', home_view, name='home'),
#     path('login/', login_view, {'popup': 'login'}, name='login'),
#     path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
#     # path('student/', student_view, name='student'),
    
#     # Redirect pages after login
#     path('student/', student_view, name='student'),
#     path('parent/', parent_view, name='parent'),
#     path('teacher/', teacher_view, name='teacher'),
#     path('principal/',principal_view, name='principal'),

#     path('logout/', logout_view, name='logout'),
#     # path('admin-panel/',adminPage, name='admin_panel'),
#     # path('add-student/', add_student, name='add_student'),
#     # path('add-teacher/', add_teacher, name='add_teacher'),


   
# ]
 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, {'popup': 'login'}, name='login'),
    path('signup/', views.signup_view, {'popup': 'signup'}, name='signup'),

    path('student/', views.student_view, name='student'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('principal/', views.principal_view, name='principal'),

    path('logout/', views.logout_view, name='logout'),

    # CRUD endpoints used by the principal (admin dashboard)
    path('add-admin/', views.add_admin, name='add_admin'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-student/', views.add_student, name='add_student'),

    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
]



