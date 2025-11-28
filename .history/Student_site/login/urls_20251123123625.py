from django.urls import path
from .views import home_view,login_view,signup_view


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
    path('student/', student, name='admins'),
]
