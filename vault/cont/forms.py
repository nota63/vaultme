from django import forms
from .models import Cont


class ContactForm(forms.ModelForm):
    relation = forms.ChoiceField(choices=Cont._meta.get_field('relation').choices)
    type = forms.ChoiceField(choices=Cont._meta.get_field('type').choices)

    class Meta:
        model = Cont
        fields = ['name', 'contact', 'relation', 'type', 'active']
