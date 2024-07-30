from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['user', 'profile_pic', 'name', 'email', 'connection', 'social_id', 'type', 'special_name']
        widgets = {
            'connection': forms.Select(choices=Person._meta.get_field('connection').choices),
            'type': forms.Select(choices=Person._meta.get_field('type').choices),
        }
