from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['task_name', 'category', 'important', 'description', 'date_to_accomplish']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }
