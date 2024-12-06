from django.shortcuts import render
from .models import Profile, Skill


def profiles(request):
    profiles = Profile.objects.all()
    Skills = Skill.objects.all()
    context = {"profiles": profiles, "skills": Skills}
    return render(request, "users/profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {
        "profile": profile,
        "topSkills": topSkills,
        "otherSkills": otherSkills,
    }
    return render(request, "users/user-profile.html", context)


# Create your views here.
