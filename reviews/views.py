from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import TicketForm
from .models import Ticket

@login_required
def feed_view(request):
    tickets=Ticket.objects.all()
    return render(request, 'reviews/feed.html',{'tickets': tickets})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST,request.FILES)
        if form.is_valid():
            ticket=form.save(commit=False)
            ticket.user=request.user #Assign the logged in user
            ticket.save()
            return redirect('ticket_succes')
    else:
        form=TicketForm()
    return render(request, 'reviews/create_ticket.html', {'form':form})

def ticket_succes(request):
    return render (request, 'reviews/ticket_succes.html')

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        form=TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'reviews/edit_ticket.html',{'form':form})
@require_POST
def delete_ticket(request, ticket_id):
    ticket=get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.delete()
    return redirect('feed')
# Create your views here.
