from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from ..models import Asignatura, AsignaturaDocente
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorator import role_required

User = get_user_model()

@login_required
@role_required(allowed_roles=['admin'])
def asignar_asignatura(request):
    if request.method == 'POST':
        docente_id = request.POST.get('docente_id')
        asignatura_id = request.POST.get('asignatura_id')

        try:
            docente = User.objects.get(id=docente_id, rol='docente')
            asignatura = Asignatura.objects.get(id=asignatura_id)

            if AsignaturaDocente.objects.filter(docente=docente, asignatura=asignatura).exists():
                messages.error(request, 'Este docente ya está asignado a esta asignatura.')
            else:
                AsignaturaDocente.objects.create(docente=docente, asignatura=asignatura)
                messages.success(request, 'Asignación realizada con éxito.')

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')

        return redirect('asignar_asignatura_admin_view')  # Redirige luego del POST

    docentes = User.objects.filter(rol='docente')
    asignaturas = Asignatura.objects.all()
    return render(request, 'core/admin_docentes_asign.html', {
        'docentes': docentes,
        'asignaturas': asignaturas,
    })