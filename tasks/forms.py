from django import forms
from .models import Task

class TaskCompletionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']

from django import forms
from .models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'github', 'linkedin']
        widgets = {
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
        }