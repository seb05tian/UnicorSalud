from django.urls import path
from .views import home, exit

urlpatterns = [
    path('', home, name='home'),
    path('logout/', exit, name='exit'),
]