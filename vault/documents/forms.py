from django import forms
from .models import Documents

from django import forms
from .models import Documents


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_id': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'is_legal': forms.Select(attrs={'class': 'form-control'}),
            'nominee': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'type_doc': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'type': 'Document Type',
            'name': 'Document Name',
            'document': 'Upload Document',
            'person_name': 'Person Name',
            'document_id': 'Document ID',
            'country': 'Country',
            'is_legal': 'Legal Status',
            'nominee': 'Nominee',
            'nominee_contact': 'Nominee Contact',
            'type_doc': 'Type of Document',
        }
