from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput
                               (attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput(
                 attrs={'class': 'form-control'}))
    
class InscriptionForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer mot de passe"

        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-input'