from django.shortcuts import render, redirect, get_object_or_404
from ..models import Programa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required
def programas_view(request):
    programas = Programa.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            try:
                Programa.objects.create(nombre=nombre)
                messages.success(request, 'Programa creado correctamente.')
            except:
                messages.error(request, 'Ya existe un programa con ese nombre.')

        return redirect('crear_programa')

    return render(request, 'core/programas.html', {'programas': programas})

@login_required
def eliminar_programa(request, programa_id):
    programa = get_object_or_404(Programa, id=programa_id)
    programa.delete()
    messages.success(request, 'Programa eliminado correctamente.')
    return redirect('crear_programa')
