from django.urls import path
from .views import index_view, login_view,signuhome_view


urlpatterns = [
    path('', home_view, name='home'),

]
