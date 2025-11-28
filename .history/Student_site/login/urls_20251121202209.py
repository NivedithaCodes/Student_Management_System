from django.urls import path
from .views import indhome_view


urlpatterns = [
    path('', home_view, name='home'),

]
