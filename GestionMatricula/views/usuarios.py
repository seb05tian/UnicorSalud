from ..models import usuarios
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from ..decorator import role_required

User = get_user_model()

@login_required
@role_required(allowed_roles=['admin'])
def usuarios_admin_view(request):
    if request.method == 'POST':
        identificacion = request.POST['identificacion']
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        rol = request.POST['rol'].lower()

        if rol not in ['estudiante', 'docente', 'admin']:
            messages.error(request, 'Rol no válido.')
            return redirect('usuarios_admin_view')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or User.objects.filter(identificacion=identificacion).exists():
            messages.error(request, 'El usuario ya existe.')
            return redirect('usuarios_admin_view')

        User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            rol=rol,
            identificacion=identificacion,
            password='usuario123'
        )

        messages.success(request, 'Usuario creado con éxito.')
        return redirect('usuarios_admin_view')  # Aquí se hace el redirect tras el POST

    return render(request, 'core/admin_usuarios.html', {
        'usuarios': usuarios.objects.all(),
    })

