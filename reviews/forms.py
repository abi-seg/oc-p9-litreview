from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    """
    Formulaire de création et de modification d'un ticket.

    Ce formulaire est basé sur le modèle 'Ticket' et permet à l'utilisateur
    d'ajouter un titre, une description et une image. Les widgets sont personnalisés
    afin d'appliquer des classes CSS pour améliorer l'affichage dans l'interface utilisateur.

    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FollowUserForm(forms.Form):

        """
        Formulaire permettant de suivre un utilisateur.

        Ce formulaire contient un seul champ : le nom d'utilisateur de la personne
        que l'on souhaite suivre. Le champ est stylisé avec des attributs CSS pour
        une meilleure présentation.

        """
        username = forms.CharField(label="Nom d'utilisateur", max_length=150,
                               widget=forms.TextInput(attrs={
                                   'class':'form-control',
                                   'placeholder': 'Nom Utilisateur',
                                   'style': 'max-width: 300px;'
                               }))


class ReviewForm(forms.ModelForm):
    """
    Formulaire de création ou d’édition d'une critique (review).

    Basé sur le modèle `Review`, ce formulaire permet de saisir un titre court
    (headline), une note (rating) et un texte descriptif (body). Le widget
    utilisé pour la note est un `RadioSelect` afin d'améliorer l'expérience
    utilisateur. Les champs « headline » et « body » sont personnalisés
    dynamiquement lors de l'initialisation pour leur appliquer des classes CSS.

    """
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating':forms.RadioSelect
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs['class'] = 'form-input'
        self.fields['body'].widget.attrs['class'] = 'form-input'