from django import forms
from .models import Asignatura, Prerrequisito

class AsignaturaForm(forms.ModelForm):
    prerequisito = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        required=False,
        label='Prerrequisito',
        
    )

    class Meta:
        model = Asignatura
        fields = ['codigo', 'nombre', 'nivel', 'programa', 'descripcion']

