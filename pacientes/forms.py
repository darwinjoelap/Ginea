from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Fieldset, Field
from .models import Paciente


def seccion(titulo):
    return HTML(f'''
        <div class="col-12 mt-4 mb-2">
          <h6 class="fw-bold text-uppercase text-muted border-bottom pb-1"
              style="font-size:0.75rem;letter-spacing:1px;color:#6f42c1!important">
            {titulo}
          </h6>
        </div>
    ''')


class PacientePersonalForm(forms.ModelForm):
    """Solo datos personales — para asistente."""
    class Meta:
        model = Paciente
        fields = [
            'nombre_completo', 'cedula', 'fecha_nacimiento', 'telefono', 'email',
            'estado_civil', 'nivel_instruccion', 'ocupacion',
            'direccion', 'contacto_emergencia', 'seguro_medico',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre_completo', css_class='col-12 col-md-8'),
                Column('cedula', css_class='col-12 col-md-4'),
            ),
            Row(
                Column('fecha_nacimiento', css_class='col-12 col-md-4'),
                Column('telefono', css_class='col-12 col-md-4'),
                Column('estado_civil', css_class='col-12 col-md-4'),
            ),
            'email',
            Row(
                Column('nivel_instruccion', css_class='col-12 col-md-6'),
                Column('ocupacion', css_class='col-12 col-md-6'),
            ),
            'direccion',
            Row(
                Column('contacto_emergencia', css_class='col-12 col-md-6'),
                Column('seguro_medico', css_class='col-12 col-md-6'),
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary btn-touch w-100 mt-3'),
        )


class PacienteCompletoForm(forms.ModelForm):
    """Ficha completa — solo doctora."""
    class Meta:
        model = Paciente
        exclude = ['creado_en', 'actualizado_en']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fur': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_ultimo_parto': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'ultima_citologia_fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'vih_fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'diu_fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'alergias': forms.Textarea(attrs={'rows': 2}),
            'enfermedades_cronicas': forms.Textarea(attrs={'rows': 2}),
            'cirugias_previas': forms.Textarea(attrs={'rows': 2}),
            'medicacion_actual': forms.Textarea(attrs={'rows': 2}),
            'its_previas': forms.Textarea(attrs={'rows': 2}),
            'menopausia_sintomas': forms.Textarea(attrs={'rows': 2}),
            'metodos_anteriores': forms.Textarea(attrs={'rows': 2}),
            'antec_autoinmunes': forms.Textarea(attrs={'rows': 2}),
            'antec_geneticas': forms.Textarea(attrs={'rows': 2}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_fields = [
            'fecha_nacimiento', 'fur', 'fecha_ultimo_parto',
            'ultima_citologia_fecha', 'vih_fecha', 'diu_fecha'
        ]
        for f in date_fields:
            if f in self.fields:
                self.fields[f].input_formats = ['%Y-%m-%d']

        # Campos opcionales
        optional = [
            'ocupacion', 'direccion', 'contacto_emergencia', 'seguro_medico',
            'alergias', 'enfermedades_cronicas', 'cirugias_previas', 'medicacion_actual',
            'grupo_sanguineo', 'antec_autoinmunes', 'antec_geneticas',
            'fur', 'fecha_ultimo_parto', 'ultima_citologia_fecha', 'ultima_citologia_resultado',
            'vih_fecha', 'its_previas', 'inicio_vida_sexual', 'num_parejas',
            'menopausia_edad', 'menopausia_sintomas', 'metodo_anticonceptivo',
            'metodo_tiempo_uso', 'metodos_anteriores', 'diu_fecha', 'diu_tipo', 'observaciones',
        ]
        for f in optional:
            if f in self.fields:
                self.fields[f].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            # ── Datos personales ──────────────────────────────────────
            seccion('Datos personales'),
            Row(
                Column('nombre_completo', css_class='col-12 col-md-8'),
                Column('cedula', css_class='col-12 col-md-4'),
            ),
            Row(
                Column('fecha_nacimiento', css_class='col-12 col-md-4'),
                Column('telefono', css_class='col-12 col-md-4'),
                Column('estado_civil', css_class='col-12 col-md-4'),
            ),
            'email',
            Row(
                Column('nivel_instruccion', css_class='col-12 col-md-6'),
                Column('ocupacion', css_class='col-12 col-md-6'),
            ),
            'direccion',
            Row(
                Column('contacto_emergencia', css_class='col-12 col-md-6'),
                Column('seguro_medico', css_class='col-12 col-md-6'),
            ),

            # ── Antecedentes personales ───────────────────────────────
            seccion('Antecedentes personales'),
            'alergias',
            'enfermedades_cronicas',
            'cirugias_previas',
            'medicacion_actual',
            Row(
                Column('grupo_sanguineo', css_class='col-6 col-md-3'),
                Column('tabaquismo', css_class='col-6 col-md-3 pt-md-4'),
                Column('alcoholismo', css_class='col-6 col-md-3 pt-md-4'),
                Column('transfusiones', css_class='col-6 col-md-3 pt-md-4'),
            ),

            # ── Antecedentes familiares ───────────────────────────────
            seccion('Antecedentes familiares'),
            Row(
                Column('antec_cancer_mama', css_class='col-6 col-md-3'),
                Column('antec_cancer_cuello', css_class='col-6 col-md-3'),
                Column('antec_diabetes', css_class='col-6 col-md-3'),
                Column('antec_hipertension', css_class='col-6 col-md-3'),
            ),
            Row(
                Column('antec_autoinmunes', css_class='col-12 col-md-6'),
                Column('antec_geneticas', css_class='col-12 col-md-6'),
            ),

            # ── Historia gineco-obstétrica ─────────────────────────────
            seccion('Historia gineco-obstétrica'),
            Row(
                Column('menarquia', css_class='col-6 col-md-3'),
                Column('ciclo_dias', css_class='col-6 col-md-3'),
                Column('ciclo_regular', css_class='col-6 col-md-3 pt-md-4'),
                Column('fur', css_class='col-6 col-md-3'),
            ),
            Row(
                Column('gestas', css_class='col-3'),
                Column('partos', css_class='col-3'),
                Column('cesareas', css_class='col-3'),
                Column('abortos', css_class='col-3'),
            ),
            Row(
                Column('fecha_ultimo_parto', css_class='col-12 col-md-4'),
                Column('ultima_citologia_fecha', css_class='col-12 col-md-4'),
                Column('ultima_citologia_resultado', css_class='col-12 col-md-4'),
            ),
            Row(
                Column('vph_diagnostico', css_class='col-6 col-md-3'),
                Column('vph_vacuna', css_class='col-6 col-md-3'),
                Column('vih_resultado', css_class='col-12 col-md-3'),
                Column('vih_fecha', css_class='col-12 col-md-3'),
            ),
            'its_previas',
            Row(
                Column('inicio_vida_sexual', css_class='col-6 col-md-3'),
                Column('num_parejas', css_class='col-6 col-md-3'),
                Column('dispareunia', css_class='col-6 col-md-3 pt-md-4'),
            ),
            Row(
                Column('menopausia', css_class='col-6 col-md-3 pt-md-4'),
                Column('menopausia_edad', css_class='col-6 col-md-3'),
                Column('menopausia_sintomas', css_class='col-12 col-md-6'),
            ),

            # ── Planificación familiar ────────────────────────────────
            seccion('Planificación familiar'),
            Row(
                Column('metodo_anticonceptivo', css_class='col-12 col-md-6'),
                Column('metodo_tiempo_uso', css_class='col-12 col-md-6'),
            ),
            'metodos_anteriores',
            Row(
                Column('deseo_embarazo', css_class='col-6 col-md-3 pt-md-4'),
                Column('ligadura', css_class='col-6 col-md-3 pt-md-4'),
                Column('diu_tipo', css_class='col-12 col-md-3'),
                Column('diu_fecha', css_class='col-12 col-md-3'),
            ),

            # ── Observaciones ─────────────────────────────────────────
            seccion('Observaciones'),
            'observaciones',

            Submit('submit', 'Guardar ficha', css_class='btn btn-primary btn-touch w-100 mt-4'),
        )
