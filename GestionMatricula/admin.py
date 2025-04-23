from django.contrib import admin
from .models import (
    usuarios, Programa, Asignatura, AsignaturaDocente,
    Prerrequisito, AsignaturaAprobada, Matricula, Reporte
)

@admin.register(usuarios)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'rol', 'is_active')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'programa', 'nivel')
    list_filter = ('programa', 'nivel')
    search_fields = ('codigo', 'nombre')

@admin.register(AsignaturaDocente)
class AsignaturaDocenteAdmin(admin.ModelAdmin):
    list_display = ('docente', 'asignatura')
    list_filter = ('docente', 'asignatura')
    search_fields = ('docente__username', 'asignatura__nombre')

@admin.register(Prerrequisito)
class PrerrequisitoAdmin(admin.ModelAdmin):
    list_display = ('asignatura', 'prerequisito')
    search_fields = ('asignatura__codigo', 'prerequisito__codigo')

@admin.register(AsignaturaAprobada)
class AsignaturaAprobadaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignatura', 'fecha_aprobacion')
    list_filter = ('fecha_aprobacion',)
    search_fields = ('estudiante__username', 'asignatura__nombre')

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignatura', 'fecha_matricula')
    list_filter = ('fecha_matricula',)
    search_fields = ('estudiante__username', 'asignatura__nombre')

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha_generacion')
    list_filter = ('fecha_generacion',)
    search_fields = ('estudiante__username', 'contenido')