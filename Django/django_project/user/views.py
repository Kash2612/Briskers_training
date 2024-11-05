from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterform, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


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

def logout(request):
    auth_logout(request)
    return render(request, 'user/logout.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Updated your profile')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)