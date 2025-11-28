from django.urls import path
from .views import sshome_view


urlpatterns = [
    path('', home_view, name='home'),

]
