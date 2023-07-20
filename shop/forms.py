from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EigeneUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['username'].label = 'Benutzername'
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].label = 'Passwort'
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].label = 'Passwort wiederholen'
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].label = 'Email'