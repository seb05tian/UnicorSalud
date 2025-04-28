from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Asignatura, Matricula, AsignaturaDocente
from ..decorator import role_required


@login_required
@role_required(allowed_roles=['docente'])
def docente_asignaturas_asignadas(request):
    user = request.user
    is_docente = user.rol == 'docente'
    is_admin = user.rol == 'admin'

    docente_id = None
    Asignaciones = []
    mostrar_resultados = False

    if is_docente:
        docente_id = user.identificacion
        Asignaciones = AsignaturaDocente.objects.filter(docente__identificacion=docente_id).select_related('asignatura')
        mostrar_resultados = True

    elif is_admin:
        estudiante_id = request.GET.get('docente_id')
        if estudiante_id:
            Asignaciones = AsignaturaDocente.objects.filter(docente__identificacion=docente_id).select_related('asignatura')
            mostrar_resultados = True

    return render(request, 'core/docente_asignaturas.html', {
        'Asignaciones': Asignaciones,
        'docente_id': docente_id,
        'is_docente': is_docente,
        'is_admin': is_admin,
        'mostrar_resultados': mostrar_resultados
    })

  

@login_required
@role_required(allowed_roles=['docente'])
def listado_estudiantes(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    estudiantes = Matricula.objects.filter(asignatura_id=asignatura_id).select_related('estudiante')

    context = {
        'asignatura': asignatura,
        'estudiantes': estudiantes,
    }
    return render(request, 'core/listado_estudiantes.html', context)