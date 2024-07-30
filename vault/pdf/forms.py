from django import forms
from .models import Pdf


class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['name', 'pdf', 'type', 'description', 'tags', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
