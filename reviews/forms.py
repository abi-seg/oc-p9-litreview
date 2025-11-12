from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FollowUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }