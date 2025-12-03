"""
URL configuration for Student_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('login.urls')),
]

from django.contrib import admin
from django.urls import path,inc
from login import views  # Replace 'core' with your app name if different

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL → principal dashboard
    path('', views.principal_dashboard, name='principal_dashboard'),

    # Admin URLs
    path('add-admin/', views.add_admin, name='add_admin'),

    # Teacher URLs
    path('add-teacher/', views.add_teacher, name='add_teacher'),

    # Student URLs
    path('add-student/', views.add_student, name='add_student'),

    # User edit/delete
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),

    # Class URLs
    path('add-class/', views.add_class, name='add_class'),
    path('edit-class/<int:id>/', views.edit_class, name='edit_class'),
    path('delete-class/<int:id>/', views.delete_class, name='delete_class'),

    # Subject URLs
    path('add-subject/', views.add_subject, name='add_subject'),
    path('edit-subject/<int:id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:id>/', views.delete_subject, name='delete_subject'),

    # Syllabus URLs
    path('add-syllabus/', views.add_syllabus, name='add_syllabus'),
    path('edit-syllabus/<int:id>/', views.edit_syllabus, name='edit_syllabus'),
    path('delete-syllabus/<int:id>/', views.delete_syllabus, name='delete_syllabus'),

    # Timetable URLs
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('edit-timetable/<int:id>/', views.edit_timetable, name='edit_timetable'),
    path('delete-timetable/<int:id>/', views.delete_timetable, name='delete_timetable'),
]


from django.db import migrations

def create_admin(apps, schema_editor):
    User = apps.get_model("core", "User")
    if not User.objects.filter(email="admin@example.com").exists():
        u = User(
            name="Administrator",
            email="admin@example.com",
            role="admin",
            password="admin123"   # ← PLAIN PASSWORD
        )
        u.save()

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]