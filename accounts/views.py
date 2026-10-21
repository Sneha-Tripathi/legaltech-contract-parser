from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account Created Successfully")

            return redirect("login")

    else:

        form = UserCreationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]

        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("login")