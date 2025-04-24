from django.urls import path, include
from rest_framework import routers
from .views import home, exit, AsignaturaViewSet, asignaturas_admin_view

router = routers.DefaultRouter()
router.register('asignaturas', AsignaturaViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('logout/', exit, name='exit'),
    path('admin_asignaturas/', asignaturas_admin_view, name='admin_asignaturas'),
    path('api/', include(router.urls)), 
]