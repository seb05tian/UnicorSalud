from django import forms
from .models import Asignatura

class AsignaturaForm(forms.ModelForm):
    
    prerrequisito = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        required=False,
        label='Prerrequisito'
    )

    class Meta:
        model = Asignatura
        fields = ['codigo', 'nombre', 'programa', 'descripcion', 'nivel']