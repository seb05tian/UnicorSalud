from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Asignatura, Matricula
from django.contrib.auth.decorators import login_required


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
    user = request.user
    is_estudiante = user.rol == 'estudiante'
    is_admin = user.rol == 'admin'

    estudiante_id = None
    matriculas = []
    mostrar_resultados = False

    if is_estudiante:
        estudiante_id = user.identificacion
        matriculas = Matricula.objects.filter(estudiante__identificacion=estudiante_id).select_related('asignatura')
        mostrar_resultados = True

    elif is_admin:
        estudiante_id = request.GET.get('estudiante_id')
        if estudiante_id:
            matriculas = Matricula.objects.filter(estudiante__identificacion=estudiante_id).select_related('asignatura')
            mostrar_resultados = True

    return render(request, 'core/asignaturas_matriculadas.html', {
        'matriculas': matriculas,
        'estudiante_id': estudiante_id,
        'is_estudiante': is_estudiante,
        'is_admin': is_admin,
        'mostrar_resultados': mostrar_resultados
    })

# Docente: Ver Estudiantes Matriculados

def ver_estudiantes_matriculados(request):
    asignaturas = request.user.asignatura_set.all()
    contexto = []
    for asignatura in asignaturas:
        matriculas = Matricula.objects.filter(asignatura=asignatura)
        contexto.append((asignatura, matriculas))
    return render(request, 'estudiantes_matriculados.html', {'asignaturas_matriculas': contexto})






