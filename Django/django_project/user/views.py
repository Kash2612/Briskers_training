from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterform


def register(request):
    if request.method == 'POST':
        form = UserRegisterform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, you can now login')
            return redirect('login')
    else:
        form =UserRegisterform()
    return render(request, 'user/register.html', {'form': form})