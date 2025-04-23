from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','descriptio','important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Titulo'}),
            'descriptio': forms.Textarea(attrs={'class': 'form-control' , 'placeholder':'Descripcion'}),
        }