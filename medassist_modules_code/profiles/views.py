
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .forms import PatientProfileForm
from .models import PatientProfile


def auth_page(request):
    if request.user.is_authenticated:
        return redirect("profile_detail")

    login_form = AuthenticationForm(request)
    register_form = UserCreationForm()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "login":
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                messages.success(request, "Login successful.")
                return redirect("profile_edit")

        elif action == "register":
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("profile_edit")

    return render(request, "registration/login.html", {
        "login_form": login_form,
        "register_form": register_form,
    })


@login_required
def profile_detail(request):
    profile = PatientProfile.objects.filter(user=request.user).first()
    if profile is None:
        return redirect("profile_edit")
    return render(request, "profiles/profile_detail.html", {"profile": profile})


@login_required
def profile_edit(request):
    profile, _ = PatientProfile.objects.get_or_create(
        user=request.user,
        defaults={"full_name": request.user.get_full_name() or request.user.get_username()},
    )

    if request.method == "POST":
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            saved_profile = form.save(commit=False)
            saved_profile.user = request.user
            saved_profile.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect("profile_detail")
    else:
        form = PatientProfileForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form})
