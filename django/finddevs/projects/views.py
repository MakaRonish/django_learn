from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .utils import searchProjects, paginateProjects

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib import messages


# projectsList = [
#     {
#         "id": "1",
#         "title": "Ecommerce Website",
#         "description": "Fully functional ecommerce website",
#     },
#     {
#         "id": "2",
#         "title": "Portfolio Website",
#         "description": "A personal website to write articles and display work",
#     },
#     {
#         "id": "3",
#         "title": "Social Network",
#         "description": "An open source project built by the community",
#     },
# ]


def projects(request):
    projects, search_query = searchProjects(request)

    # page = request.GET.get("page")  # query string
    # result = 3
    # paginator = Paginator(projects, result)

    # try:
    #     projects = paginator.page(page)
    # except PageNotAnInteger:
    #     page = 1
    #     projects = paginator.page(page)
    # except EmptyPage:
    #     page = paginator.num_pages  # gives the number of page
    #     projects = paginator.page(page)

    # leftIndex = int(page) - 4
    # if leftIndex < 1:
    #     leftIndex = 1

    # rightIndex = int(page) + 5
    # if rightIndex > paginator.num_pages:
    #     rightIndex = paginator.num_pages

    # custom_range = range(leftIndex, rightIndex + 1)

    projects, custom_range, paginator = paginateProjects(request, projects, 9)
    context = {
        "projectsList": projects,
        "search_query": search_query,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    form = ReviewForm()
    context = {"projectObj": projectObj, "tags": tags, "form": form}

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, "Review submitted")
        return redirect("project", pk=projectObj.id)

    # projectObj = None
    # for i in projectsList:
    #     if i["id"] == str(pk):
    #         projectObj = i
    # print("hello")
    # print(projectObj)
    return render(request, "projects/single-project.html", context)


# Create your views here.


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile  # so other user cant edit
    project = profile.project_set.get(id=pk)
    # project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile  # so other user cant edit
    project = profile.project_set.get(id=pk)
    # project = Project.objects.get(id=pk)
    context = {"object": project}
    if request.method == "POST":
        project.delete()
        return redirect("account")

    return render(request, "delete_template.html", context)
