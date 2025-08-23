from django import forms
from .models import Alerte

class AlerteForm(forms.ModelForm):
    class Meta:
        model = Alerte
        fields = ['reference', 'zone_kit', 'nombre_bacs', 'commentaires']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'zone_kit': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('zone_1', 'Zone 1'),
                ('zone_2', 'Zone 2'),
                ('zone_3', 'Zone 3'),
                ('zone_4', 'Zone 4'),
                ('zone_5', 'Zone 5'),
                ('zone_6', 'Zone 6'),
                ('zone_7', 'Zone 7'),
                ('zone_8', 'Zone 8'),
                ('zone_9', 'Zone 9'),
                ('zone_10', 'Zone 10'),
                ('zone_11', 'Zone 11'),
            ]),
            'nombre_bacs': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'commentaires': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }