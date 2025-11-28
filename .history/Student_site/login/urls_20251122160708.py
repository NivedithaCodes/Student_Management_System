from django.urls import path
from .views import home_view,login_view,signup_view,admin


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='signup'),
    path('admin/', admin_view, name='admin'),
]
