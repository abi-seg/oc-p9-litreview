from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket

@login_required
def feed_view(request):
    return render(request, 'reviews/feed.html')

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.post,request.files)
        if form.is_valid():
            ticket=form.save(commit=False)
            ticket.user=request.user #Assign the logged in user
            ticket.save()
            return redirect('ticket_success')
    else:
        form=TicketForm()
    return render(request, 'reviews/create_ticket.html', {'form':form})

def ticket_succes(request):
    return render (request, 'reviews/ticket_succes.html')

# Create your views here.
