import pandas as pd
from django.http import HttpResponse
from ..models import Matricula
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..decorator import role_required

def exportar_reporte_excel(request):
    if not request.user.is_authenticated or request.user.rol != 'admin':
        return HttpResponse("No autorizado", status=403)
    matriculas = Matricula.objects.select_related('estudiante', 'asignatura').all()

    
    data = []
    for matricula in matriculas:
        data.append({
            'Identificacion': matricula.estudiante.identificacion,
            'Nombre': matricula.estudiante.first_name,
            'Apellido': matricula.estudiante.last_name,
            'Programa': matricula.estudiante.programa.nombre if matricula.estudiante.programa else '',
            'Nivel (Semestre)': matricula.estudiante.nivel,
            'Asignatura': matricula.asignatura.nombre,
        })

    df = pd.DataFrame(data)

    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_matriculas.xlsx"'

    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        
        df.to_excel(writer, index=False, sheet_name='Todos')

        
        if 'Programa' in df.columns:
            for programa, datos_programa in df.groupby('Programa'):
                nombre_hoja = programa if programa else "Sin Programa"
                datos_programa.to_excel(writer, index=False, sheet_name=nombre_hoja[:31])  # Excel limita el nombre de hoja a 31 caracteres

        
        if 'Nivel (Semestre)' in df.columns:
            for nivel, datos_nivel in df.groupby('Nivel (Semestre)'):
                nombre_hoja = f"Nivel {nivel}" if nivel else "Sin Nivel"
                datos_nivel.to_excel(writer, index=False, sheet_name=nombre_hoja[:31])

       
        if 'Asignatura' in df.columns:
            for asignatura, datos_asignatura in df.groupby('Asignatura'):
                nombre_hoja = asignatura if asignatura else "Sin Asignatura"
                datos_asignatura.to_excel(writer, index=False, sheet_name=nombre_hoja[:31])

    return response


@login_required
@role_required(allowed_roles=['admin'])
def pagina_reporte_admin(request):
    if not request.user.is_authenticated or request.user.rol != 'admin':
        return HttpResponse("No autorizado", status=403)
    return render(request, 'core/reporte_admin.html')