from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import ConnexionForm, InscriptionForm
from django.contrib.auth.forms import AuthenticationForm

def connexion_view(request):
    """
    Gère la connexion d'un utilisateur.
    si la méthode est POST, vérifie les informations de connnexion avec la formulaire personnalisé.
    si elles sont valides, connecte l'utilisateur et le redirige vers la page du flux.
    sinon, affiche le formulaire de connexion.
    : param request: HttpRequest de Django
    : return: Page de connexion avec formulaire ou redirection

    """
    if request.method == 'POST':
        form = ConnexionForm(request, data = request.POST)
        if form.is_valid():
            
            login(request,form.get_user())
            return redirect('feed')
    else:
        form = ConnexionForm()
    return render(request, 'accounts/connexion.html', {'form': form})

def inscription_view(request):
     """
     Gère l'inscription d'un nouvel utilisateur.

     si la méthode est POST et que le formulaire est valide,
     l'utilisateur est enregistré, connecté automatiquement, puis redirigé vers le flux.
     sinon, affiche le formulaire d'inscription vide ou avec erreurs.
     :param request: HttpRequest de Django
     :return: Page d'inscription avec formulaire ou redirection
     
     """
     if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
     else:
        form = InscriptionForm()
     return render(request, 'accounts/inscription.html',{'form':form})
# Create your views here.
