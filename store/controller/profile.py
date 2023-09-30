
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Profile
from store.forms import ProfileForm , ProfileImageForm 


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("view_profile")
    else:
        form = ProfileForm(instance=profile)

    context = {"profile": profile, "form": form}
    return render(request, "store/profile.html", context)


def delete_profile_image(request):
    if request.method == "POST" and request.user.is_authenticated:
        # Get the user's profile
        profile = Profile.objects.get(user=request.user)

        # Check if a profile image exists
        if profile.image:
            # Delete the profile image
            profile.image.delete()
            # Save the profile without the image
            profile.save()
    
    # Redirect back to the profile page
    return redirect("/profile")


def update_profile_image(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to the profile page after a successful update
            return redirect("/profile")
    else:
        form = ProfileImageForm()

    context = {"form": form}
    return render(request, "store/profile_image_upload.html", context)