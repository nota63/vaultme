from django import forms
from .models import Passwords


class PasswordForm(forms.ModelForm):
    class Meta():
        model = Passwords
        fields = ['your_name', 'username', 'password', 'type', 'type_name', 'id_name',
                  'is_active', 'description', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'username': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'password': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }
