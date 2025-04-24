from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import usuarios, Asignatura, Matricula, AsignaturaAprobada, Prerrequisito, Reporte
from ..serializer import AsignaturaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

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

class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer
    permission_classes = [IsAuthenticated]
    
@login_required
def asignaturas_admin_view(request):
    return render(request, 'core/admin_asignatura.html')