from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Crée l'utilisateur
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
