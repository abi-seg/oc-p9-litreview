from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import TicketForm,ReviewForm,FollowUserForm
from .models import Ticket,Review,UserFollows
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model

@login_required

def feed_view(request):
    tickets=Ticket.objects.all().order_by('-time_created')
    reviews=Review.objects.all().order_by('-time_created')
    return render(request, 'reviews/feed.html',
                  {'tickets': tickets,
                    'reviews': reviews})
   

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
            updated_ticket =  form.save(commit=False)
            print("Before Save:",updated_ticket.id, updated_ticket.title)
            updated_ticket.user=request.user #Reassign ownership here
            updated_ticket.save()
            print("After save:",updated_ticket.id)
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'reviews/edit_ticket.html',{'form':form, 'ticket':ticket})

@require_POST
def delete_ticket(request, ticket_id):
    ticket=get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.delete()
    return redirect('feed')


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Optional: check if user has already reviewed this ticket
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        # Handle this: redirect, error message, etc.
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {
        'form': form,
        'ticket': ticket
    })

@login_required
def select_ticket_to_review(request):
    user = request.user
    reviewed_ticket_ids = Review.objects.filter(user=user).values_list('ticket_id', flat=True)
    tickets = Ticket.objects.exclude(user=user).exclude(id__in=reviewed_ticket_ids)
    return render(request, 'reviews/select_ticket_to_review.html',{'tickets': tickets})

def create_ticket_and_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form=ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user=request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket # link review to the newly created ticket
            review.save()

            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'reviews/create_ticket_and_review.html',{
        'ticket_form': ticket_form,
        'review_form' : review_form
    })

User = get_user_model()

@login_required
def follow_users_view(request):
    form = FollowUserForm()
    
    followed_users = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)  #  fixed field name

    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username_to_follow = form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username_to_follow)  #  fixed "user" to "User"
                if user_to_follow == request.user:
                    messages.warning(request, " Vous ne pouvez pas vous suivre vous-même.")
                elif UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():  # ✅ field fixed
                    messages.info(request, f"Vous suivez déjà {username_to_follow}.")
                else:
                    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)  #  fixed field name
                    messages.success(request, f"Vous suivez maintenant {username_to_follow}.")
                    return redirect('follow_users')
            except User.DoesNotExist:
                messages.error(request, f"Utilisateur '{username_to_follow}' introuvable.")

    context = {
        'form': form,
        'followed_users': followed_users,
        'followers': followers,
    }
    return render(request, 'reviews/follow_users.html', context)

@login_required
def unfollow_user_view(request, follow_id):
    try:
        relation = UserFollows.objects.get(id=follow_id, user=request.user)
        username = relation.followed_user.username
        relation.delete()
        messages.success(request, f"Vous ne suivez plus {username}.")
    except UserFollows.DoesNotExist:
        messages.error(request, "Cette relation n'existe pas ou ne vous appartient pas.")
    return redirect('follow_users')