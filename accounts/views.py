from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import ConnexionForm, InscriptionForm
from django.contrib.auth.forms import AuthenticationForm

def connexion_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            
            login(request,form.get_user())
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/connexion.html', {'form': form})

def inscription_view(request):
     if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('connexion')
     else:
        form = InscriptionForm()
     return render(request, 'accounts/inscription.html',{'form':form})
# Create your views here.
