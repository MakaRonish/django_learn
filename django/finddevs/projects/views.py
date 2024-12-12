from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Review, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


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
    projects = Project.objects.all()
    page = "Project "
    number = 10
    rangee = [i for i in range(1, 11)]
    print(page)
    context = {
        "Page": page,
        "Number": number,
        "projectsList": projects,
        "range": rangee,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()

    # projectObj = None
    # for i in projectsList:
    #     if i["id"] == str(pk):
    #         projectObj = i
    # print("hello")
    # print(projectObj)
    return render(
        request,
        "projects/single-project.html",
        {"projectObj": projectObj, "tags": tags},
    )


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
            return redirect("projects")
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

    return render(request, "projects/delete_template.html", context)
