from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class ConnexionForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé.

    Cette classe étend le formulaire d'authentificaiton par défaut de Django
    afin de personnaliser l'affichage des champs <<Nom d'utilisateur>> et <<Mot de passe>>.
    Elle applique également des classes CSS spécifiques aux widgets pour
    facilitier l'intégration dans l'interface utilisateur.

    """

    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput
                               (attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput(
                 attrs={'class': 'form-control'}))
    
class InscriptionForm(UserCreationForm):
    """

    Formulaire d'inscription personnalisé.

    Cette classe étend le formulaire de création d'utilisateur de Django afin d'utilisateur
    le modèle 'CustomUser' défini dans l'application. Elle permet de personnaliser les labels des champs
    ainsi que les classes CSS des widgets pour un rendu cohérent avec le style de l'application.

    """
    class Meta:
        model = CustomUser
        fields = ['username']

        """
        Initialise le formulaire en modifiant les labels et les attributs des widgets
        pour les champs <<Nom d'utilisateur>>, <<Mot de passe>> et
        <<Confirmer mot de passe>>.

        """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer mot de passe"

        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-input'