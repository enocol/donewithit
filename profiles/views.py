from django.shortcuts import render

# Create your views here.

def profile(request):
    """
    Render the user profile page.
    """
    return render(request, 'profiles/profile.html')
