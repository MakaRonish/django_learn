from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

from django.db.models import Q

from .utils import searchProfiles, paginateProfiles

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def profiles(request):
    profiles, search_query = searchProfiles(request)

    profiles, custom_range = paginateProfiles(request, profiles, 1)

    # profiles = Profile.objects.all()
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
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
        username = request.POST["username"].lower()
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user name doesnt exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # create a session for user
            return redirect(request.GET["next"] if "next" in request.GET else "account")
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


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    context = {"form": form}
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile

            skill.save()
            messages.success(request, "New skill added")

            return redirect("account")
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    form = SkillForm(instance=skill)
    context = {"form": form}
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            messages.success(request, " skill updated")
            form.save()

            return redirect("account")
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    context = {"object": skill}
    if request.method == "POST":
        skill.delete()
        messages.success(request, " skill deleted")
        return redirect("account")
    return render(request, "delete_template.html", context)


# def editSkill(request, pk):
#     profile = request.user.profile
#     skill = Skill.objects.get(id=pk)
#     form = SkillForm(instance=skill)
#     context = {"form": form}
#     return render(request, "users/skill_form.html")


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()  # messages is from related name
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def createMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, "Message was successfully sent!!")
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)


# Create your views here.
