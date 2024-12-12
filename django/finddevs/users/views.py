from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Skill
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileForm, SkillForm


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


def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user name doesnt exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # create a session for user
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is inccorect")
    return render(request, "users/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "Log out complete")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created")
            login(request, user)
            return redirect("edit-account")
        else:
            messages.success(request, "An error has occur")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    Skills = profile.skill_set.all()

    context = {
        "profile": profile,
        "Skills": Skills,
    }
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {"form": form}
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    return render(request, "users/profile_form.html", context)


def addSkill(request):
    profile = request.user.profile
    form = SkillForm()
    context = {"form": form}
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile

            skill.save()

            return redirect("account")
    return render(request, "users/skill_form.html", context)


# Create your views here.
