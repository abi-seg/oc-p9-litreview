from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import TicketForm,ReviewForm,FollowUserForm
from .models import Ticket,Review,UserFollows
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from itertools import chain
from django.http import HttpResponseForbidden

@login_required

def feed_view(request):
# get the users that the current user is following
    followed_users = UserFollows.objects.filter(user=request.user).values_list(
        'followed_user',flat=True)
#get tickets: created by myself and created by people i follow
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_users)
    )
# get reviews: written by myself, written about tickets created by people i follow
    reviews=Review.objects.filter(
        Q(user=request.user) | Q(ticket__user__in=followed_users)
    )
#Annotate each item with a type for template logic
    combined = list(chain(
        [{'type': 'ticket','content':ticket} for ticket in tickets],
        [{'type': 'review','content':review} for review in reviews],
    ))
# sort by creation date (newest first)
    items = sorted(combined, key=lambda x: x['content'].time_created,
        reverse=True
    )
    return render(request, 'reviews/feed.html',
                  {'items':items})
   

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
        messages.warning(request, "Vous avez déjà rédigé une critique pour ce ticket.")
        # Handle this: redirect, error message, etc.
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a été publiée avec succès !")
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

@login_required
def posts_view(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    from itertools import chain
    items = sorted(
        chain(
            [{'type': 'ticket', 'content': t} for t in tickets],
            [{'type': 'review', 'content': r} for r in reviews]
        ),
        key=lambda x:x['content'].time_created,
        reverse=True
    )
    return render(request,'reviews/posts.html', {
        'items':items
    })
@login_required
def edit_review(request,review_id):
    review = get_object_or_404(Review,id=review_id,user=request.user)
    if review.user != request.user:
        return HttpResponseForbidden("You cannot edit someone else's review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST,instance = review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = ReviewForm(instance = review)

    return render(request, 'reviews/edit_review.html',{
        'form' : form,
        'review': review
    })

@require_POST
@login_required

def delete_review(request, review_id):
    review = get_object_or_404(Review, id = review_id, user = request.user)
    review.delete()
    return redirect('posts')