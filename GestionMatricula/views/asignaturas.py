from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import usuarios, Asignatura, Matricula, AsignaturaAprobada, Prerrequisito, Reporte
from ..forms import AsignaturaForm
from ..decorator import role_required

# Estudiante: Ver Asignaturas y Matricular
# Ver Asignaturas disponibles
@login_required
@role_required(allowed_roles=['estudiante'])
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
@role_required(allowed_roles=['admin'])
def asignaturas_admin_view(request):
    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            asignatura = form.save()
            
            prerrequisito = form.cleaned_data.get('prerrequisito')
            if prerrequisito:
                Prerrequisito.objects.create(
                    asignatura=asignatura,
                    prerequisito=prerrequisito
                )
            return redirect('asignaturas_admin')
    else:
        form = AsignaturaForm()

    asignaturas = Asignatura.objects.all()
    return render(request, 'core/admin_asignatura.html', {
        'form': form,
        'asignaturas': asignaturas,
    })

@login_required
@role_required(allowed_roles=['admin'])
def editar_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)

   
    prerrequisito_obj = Prerrequisito.objects.filter(asignatura=asignatura).first()

    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            asignatura = form.save()
            prerequisito = form.cleaned_data.get('prerequisito')

           
            if prerrequisito_obj:
                if prerequisito:
                    prerrequisito_obj.prerequisito = prerequisito
                    prerrequisito_obj.save()
                else:
                    prerrequisito_obj.delete()
            else:
                if prerequisito:
                    Prerrequisito.objects.create(asignatura=asignatura, prerequisito=prerequisito)

            return redirect('asignaturas_admin')
    else:
        
        initial_data = {}
        if prerrequisito_obj:
            initial_data['prerequisito'] = prerrequisito_obj.prerequisito

        form = AsignaturaForm(instance=asignatura, initial=initial_data)

    asignaturas = Asignatura.objects.all()
    return render(request, 'core/admin_asignatura.html', {
        'form': form,
        'asignaturas': asignaturas
    })


@login_required
@role_required(allowed_roles=['admin'])
def eliminar_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    asignatura.delete()
    return redirect('asignaturas_admin')
