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


f

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