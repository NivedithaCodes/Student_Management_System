from django.urls import path
from .views import index_view, login_view,signup_view,home_view


urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, {'popup': 'login'}, name='login'),
    path('signup/', signup_view, {'popup': 'signup'}, name='
    path('', home_view, name='home'),

]
