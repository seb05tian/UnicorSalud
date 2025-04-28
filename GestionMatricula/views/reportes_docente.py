from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd
from openpyxl import Workbook
from io import BytesIO
from ..models import Matricula, AsignaturaDocente
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..decorator import role_required


@login_required
def exportar_estudiantes_por_asignatura_docente(request):
    docente = request.user

    
    if docente.rol != 'docente':
        return HttpResponse("No tienes permiso para acceder a este recurso.", status=403)

   
    asignaturas_docente = AsignaturaDocente.objects.filter(docente=docente)

   
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')

    for asignatura_doc in asignaturas_docente:
        asignatura = asignatura_doc.asignatura

      
        matriculas = Matricula.objects.filter(asignatura=asignatura)

       
        data = []
        for matricula in matriculas:
            estudiante = matricula.estudiante
            data.append({
                'Identificacion': estudiante.identificacion,
                'Nombre': estudiante.first_name,
                'Apellido': estudiante.last_name,
                'Nivel (Semestre)': estudiante.nivel,
            })

       
        df = pd.DataFrame(data)

     
        nombre_hoja = asignatura.nombre[:31]  

        if not df.empty:
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
        else:
            
            pd.DataFrame([{'Mensaje': 'No hay estudiantes inscritos en esta asignatura.'}]).to_excel(writer, sheet_name=nombre_hoja, index=False)

    writer._save()

    output.seek(0)

    
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=estudiantes_por_asignatura.xlsx'
    return response

@login_required
@role_required(allowed_roles=['docente'])
def pagina_reporte_docente(request):
    if not request.user.is_authenticated or request.user.rol != 'docente':
        return HttpResponse("No autorizado", status=403)
    return render(request, 'core/reporte_docente.html')