from django.shortcuts import render
from .models import Profile, Skill


def profiles(request):
    profiles = Profile.objects.all()
    Skills = Skill.objects.all()
    context = {"profiles": profiles, "skills": Skills}
    return render(request, "users/profiles.html", context)


# Create your views here.
