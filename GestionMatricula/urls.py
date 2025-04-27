from django.urls import path, include
from rest_framework import routers

from .views.matricula import matricular_asignatura,asignaturas_matriculadas
from .views.asignaturas import  asignaturas_admin_view, ver_asignaturas_disponibles, editar_asignatura, eliminar_asignatura
from .views.logout import exit
from .views.home import home
from .views.usuarios import usuarios_admin_view
from .views.programa import programas_view,  eliminar_programa
from .views.docente import docente_asignaturas_asignadas, listado_estudiantes
from .views.docentes_asig import asignar_asignatura
from .views.reportes_admin import exportar_reporte_excel
from .views.reportes_docente import exportar_estudiantes_por_asignatura_docente


urlpatterns = [
    path('', home, name='home'),
    path('logout/', exit, name='exit'),

    path('gestion_docente/asignaturas', docente_asignaturas_asignadas, name='asignaturas_docente'),
    path('gestion_docente/listado/<int:asignatura_id>/inscritos/', listado_estudiantes, name='listado_estudiantes'),
    path('gestion_docente/reporte_docente/exportar_excel_docente/', exportar_estudiantes_por_asignatura_docente, name='listado_docente'),

    path('gestion_academica/asignaturas', asignaturas_admin_view, name='asignaturas_admin_view'),
    path('gestion_academica/usuarios', usuarios_admin_view, name='usuarios_admin_view'),
    path('gestion_academica/programa/', programas_view, name='programa_admin_view'),    
    path('gestion_academica/asignar-asignatura/', asignar_asignatura, name='asignar_asignatura_admin_view'),

    path('gestion_admin/asignaturas/', asignaturas_admin_view, name='asignaturas_admin'),
    path('gestion_admin/asignaturas/editar/<int:pk>/', editar_asignatura, name='editar_asignatura_admin'),
    path('gestion_admin/asignaturas/eliminar/<int:pk>/', eliminar_asignatura, name='eliminar_asignatura_admin'),
    path('gestion_admin/reporte/exportar_excel/', exportar_reporte_excel, name='exportar_excel'),


    path('matricula/', ver_asignaturas_disponibles, name='ver_asignaturas_disponibles'),
    path('matricular/<int:asignatura_id>/', matricular_asignatura, name='matricular_asignatura'),

    path('asignaturas/', asignaturas_matriculadas, name='asignaturas_matriculadas'),

 
    path('eliminar_programa/<int:programa_id>/', eliminar_programa, name='eliminar_programa'),


   
]