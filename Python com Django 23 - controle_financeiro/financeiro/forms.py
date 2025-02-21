from django import forms
from .models import Receita, Despesa

class ReceitaForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'class': 'form-control'}),
        input_formats=['%d/%m/%Y']
    )

    class Meta:
        model = Receita
        fields = ['nome', 'valor', 'data']

class DespesaForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'class': 'form-control'}),
        input_formats=['%d/%m/%Y']
    )

    class Meta:
        model = Despesa
        fields = ['nome', 'valor', 'data']
