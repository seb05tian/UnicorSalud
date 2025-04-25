from django.urls import path, include
from rest_framework import routers
from .views.matricula import matricular_asignatura,asignaturas_matriculadas
from .views.asignaturas import AsignaturaViewSet, asignaturas_admin_view, ver_asignaturas_disponibles
from .views.logout import exit
from .views.home import home
from .views.programa import programas_view,  eliminar_programa

router = routers.DefaultRouter()
router.register('asignaturas', AsignaturaViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('logout/', exit, name='exit'),

    path('gestion_academica/asignaturas', asignaturas_admin_view, name='asignaturas_admin_view'),

    path('matricula/', ver_asignaturas_disponibles, name='ver_asignaturas_disponibles'),
    path('matricular/<int:asignatura_id>/', matricular_asignatura, name='matricular_asignatura'),

    path('asignaturas/', asignaturas_matriculadas, name='asignaturas_matriculadas'),

    path('crear_programa/', programas_view, name='crear_programa'),
 
    path('eliminar_programa/<int:programa_id>/', eliminar_programa, name='eliminar_programa'),


    path('api/', include(router.urls)), 
]