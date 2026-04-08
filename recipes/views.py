from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Needed for OR queries
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm

def recipe_list(request):
    
    recipes = Recipe.objects.all()
    query = request.GET.get('q')  # search input
    selected_cuisine = request.GET.get('cuisine')  # selected cuisine

    if query:
        # Search recipes by name or ingredient
        recipes = recipes.filter(
            Q(name__icontains=query) | Q(ingredients__name__icontains=query)
        ).distinct()

    if selected_cuisine:
        recipes = recipes.filter(cuisine__icontains=selected_cuisine)

    # Get all distinct cuisines for the dropdown
    cuisines = Recipe.objects.values_list('cuisine', flat=True).distinct().order_by('cuisine')

    return render(request, 'recipes/list.html', {
        'recipes': recipes,
        'query': query,
        'selected_cuisine': selected_cuisine,
        'cuisines': cuisines,
    })


def recipe_detail(request, id):

    #Display details for a single recipe.

    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/detail.html', {'recipe': recipe})


def register(request):

    #Handle user registration.

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome 🎉")
            return redirect('recipe_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'recipes/register.html', {'form': form})


@login_required
def add_to_wishlist(request, id):
    
    #Add a recipe to the user's wishlist.
    recipe = get_object_or_404(Recipe, id=id)
    Wishlist.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('recipe_detail', id=id)


@login_required
def wishlist(request):

    #Display all wishlist items for the logged-in user.
        
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'recipes/wishlist.html', {'items': items})