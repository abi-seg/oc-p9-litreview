from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def feed_view(request):
    return render(request, 'reviews/feed.html')

# Create your views here.
