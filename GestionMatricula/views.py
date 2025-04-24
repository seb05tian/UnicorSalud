from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import usuarios, Asignatura, Matricula, AsignaturaAprobada, Prerrequisito, Reporte
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .serializer import AsignaturaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import  permission_classes
from rest_framework import viewsets
@login_required
def home(request):
    return render(request, 'core/home.html')


# Estudiante: Ver Asignaturas y Matricular
# Ver Asignaturas disponibles
@login_required
def ver_asignaturas_disponibles(request):
    aprobadas = AsignaturaAprobada.objects.filter(estudiante=request.user).values_list('asignatura_id', flat=True)
    ya_matriculadas = Matricula.objects.filter(estudiante=request.user).values_list('asignatura_id', flat=True)
    asignaturas = Asignatura.objects.exclude(id__in=aprobadas).exclude(id__in=ya_matriculadas)

    asignaturas_finales = []
    for asignatura in asignaturas:
        prereqs = Prerrequisito.objects.filter(asignatura=asignatura)
        if all(p.prerequisito.id in aprobadas for p in prereqs):
            asignaturas_finales.append(asignatura)

    return render(request, 'core/asignaturas_disponibles.html', {'asignaturas': asignaturas_finales})


# Proceso para matricularse los estudiantes

def matricular_asignatura(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    ya_matriculado = Matricula.objects.filter(estudiante=request.user, asignatura=asignatura).exists()
    if not ya_matriculado:
        Matricula.objects.create(estudiante=request.user, asignatura=asignatura)
        messages.success(request, f"Te has matriculado en {asignatura.nombre}.")
    else:
        messages.info(request, f"Ya estás matriculado en {asignatura.nombre}.")
    return redirect('ver_asignaturas_disponibles')

# visualizar las materias matriculadas.

@login_required
def asignaturas_matriculadas(request):
   
    matriculas = Matricula.objects.select_related('asignatura').filter(estudiante=request.user)
    return render(request, 'core/asignaturas_matriculadas.html', {'matriculas': matriculas})



# Docente: Ver Estudiantes Matriculados

def ver_estudiantes_matriculados(request):
    asignaturas = request.user.asignatura_set.all()
    contexto = []
    for asignatura in asignaturas:
        matriculas = Matricula.objects.filter(asignatura=asignatura)
        contexto.append((asignatura, matriculas))
    return render(request, 'estudiantes_matriculados.html', {'asignaturas_matriculas': contexto})



class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer
    permission_classes = [IsAuthenticated]
    
@login_required
def asignaturas_admin_view(request):
    return render(request, 'core/gestion_academica.html')


def exit(request):
    logout(request)
    return redirect('login')
