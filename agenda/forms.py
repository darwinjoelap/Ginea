from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML
from .models import Cita, LugarConsulta


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha', 'hora_inicio', 'hora_fin', 'lugar', 'motivo', 'estado', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'notas': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].input_formats = ['%Y-%m-%d']
        self.fields['hora_inicio'].input_formats = ['%H:%M']
        self.fields['hora_fin'].input_formats = ['%H:%M']
        self.fields['lugar'].queryset = LugarConsulta.objects.filter(activo=True)
        self.fields['lugar'].required = False
        self.fields['lugar'].empty_label = '— Sin especificar —'
        self.fields['notas'].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('paciente', css_class='form-select'),
            Row(
                Column('fecha', css_class='col-12 col-md-4'),
                Column('hora_inicio', css_class='col-6 col-md-4'),
                Column('hora_fin', css_class='col-6 col-md-4'),
            ),
            Row(
                Column('lugar', css_class='col-12 col-md-6'),
                Column('estado', css_class='col-12 col-md-6'),
            ),
            'motivo',
            'notas',
            Submit('submit', 'Guardar cita', css_class='btn btn-primary btn-touch w-100 mt-3'),
        )

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
        return cleaned_data
