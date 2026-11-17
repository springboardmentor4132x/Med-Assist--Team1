from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PatientProfileForm
from .models import PatientProfile

@login_required
def profile_detail(request):
    profile = PatientProfile.objects.filter(user=request.user).first()
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
