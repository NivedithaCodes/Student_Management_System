from django.urls import path
from .views import index_view, login_view,signup_view,home_view


urlpatterns = [
    path('', index_view, name='inde
    path('', home_view, name='home'),

]
