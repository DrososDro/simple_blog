from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from accounts import forms
from accounts.decorators import is_auth, is_unauth


@is_unauth
def login_user(request):
    """Login method for the user to login in the app"""
    if request.method == "POST":
        email = request.POST.get("email_id", None)
        passwd = request.POST.get("password_id", None)
        user = authenticate(request, username=email, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}")
            return redirect("home")

        else:
            messages.error(request, "Bad credentials try again")

    return render(request, "accounts/login.html")


@is_auth
def logout_urer(request):
    logout(request)
    messages.success(request, "You Successfully log out")
    return redirect("home")


# @is_unauth
def register_user(request):
    form = forms.RegisterForm()

    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.is_active = True
            form.save()
            messages.success(request, "You Successfully Sign Up")
            return redirect("login")

    context = {
        "form": form,
    }

    return render(request, "accounts/register.html", context)
