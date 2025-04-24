from django.contrib.auth import logout
from django.shortcuts import redirect

def exit(request):
    logout(request)
    return redirect('login')
