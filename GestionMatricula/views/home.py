from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def no_autorizado(request):
    return render(request, 'core/no_autorizado.html')