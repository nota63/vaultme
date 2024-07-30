from django import forms
from .models import Private



class PrivateForm(forms.ModelForm):
    class Meta:
        model = Private
        fields = ['image', 'name', 'description', 'category', 'tags', 'size']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a description'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
            'size': forms.NumberInput(attrs={'placeholder': 'Size in bytes'}),
        }
        labels = {
            'image': 'Image',
            'name': 'Name',
            'description': 'Description',
            'category': 'Category',
            'tags': 'Tags',
            'size': 'Size (bytes)',
        }
        help_texts = {
            'tags': 'Add tags separated by commas.',
            'size': 'Size in bytes, leave blank if unknown.',
        }

    def __init__(self, *args, **kwargs):
        # Automatically set the user field if not provided
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user