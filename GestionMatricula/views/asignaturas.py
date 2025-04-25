from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import usuarios, Asignatura, Matricula, AsignaturaAprobada, Prerrequisito, Reporte
from ..forms import AsignaturaForm

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

@login_required
def asignaturas_admin_view(request):
    asignaturas = Asignatura.objects.all()
    form = AsignaturaForm()

    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignaturas_admin')

    return render(request, 'core/admin_asignatura.html', {
        'asignaturas': asignaturas,
        'form': form,
    })

@login_required
def editar_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            return redirect('asignaturas_admin')
    else:
        form = AsignaturaForm(instance=asignatura)

    asignaturas = Asignatura.objects.all()
    return render(request, 'core/admin_asignatura.html', {
        'form': form,
        'asignaturas': asignaturas
    })


@login_required
def eliminar_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    asignatura.delete()
    return redirect('asignaturas_admin')