from django.urls import path, include
from rest_framework import routers
from .views import home, exit, AsignaturaViewSet, asignaturas_admin_view, ver_asignaturas_disponibles,matricular_asignatura,asignaturas_matriculadas

router = routers.DefaultRouter()
router.register('asignaturas', AsignaturaViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('logout/', exit, name='exit'),
    path('gestion_academica/', asignaturas_admin_view, name='gestion_academica'),
    path('asignaturas_disponibles/', ver_asignaturas_disponibles, name='ver_asignaturas_disponibles'),
    path('matricular/<int:asignatura_id>/', matricular_asignatura, name='matricular_asignatura'),
    path('asignaturas_matriculadas/', asignaturas_matriculadas, name='asignaturas_matriculadas'),
    path('api/', include(router.urls)), 
]