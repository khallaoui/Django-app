from django import forms
from .models import Reference, Travee


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = '__all__'
        widgets = {
            'date_entree': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'emplacement_sm': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_bacs': forms.NumberInput(attrs={'class': 'form-control'}),
            'travee_debord': forms.TextInput(attrs={'class': 'form-control'}),
            'code_condi': forms.TextInput(attrs={'class': 'form-control'}),
            'qt_piece_uc': forms.NumberInput(attrs={'class': 'form-control'}),
            'appro': forms.TextInput(attrs={'class': 'form-control'}),
            'fournisseur': forms.TextInput(attrs={'class': 'form-control'}),
            'cmj': forms.TextInput(attrs={'class': 'form-control'}),
            'f': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SortieForm(forms.Form):
    reference = forms.ModelChoiceField(
        queryset=Reference.objects.all(), 
        label="Référence",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nombre_bacs = forms.IntegerField(
        min_value=1, 
        label="Nombre de bacs à sortir",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class ViderTraveeForm(forms.Form):
    travee = forms.ModelChoiceField(
        queryset=Travee.objects.all(), 
        label="Travée à vider",
        widget=forms.Select(attrs={'class': 'form-control'})
    )