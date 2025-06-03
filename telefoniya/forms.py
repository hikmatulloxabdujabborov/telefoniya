from django import forms
from .models import Tolov, Abonent


class AbonentForm(forms.ModelForm):
    class Meta:
        model = Abonent
        fields = ['FIO', 'telefon', 'tarif', 'status']
        widgets = {
            'FIO': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'tarif': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TolovForm(forms.ModelForm):
    class Meta:
        model = Tolov
        fields = ['abonent', 'summa']
        widgets = {
            'abonent': forms.Select(attrs={'class': 'form-control'}),
            'summa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }