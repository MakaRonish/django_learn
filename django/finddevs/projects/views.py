from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {
        "id": "1",
        "title": "Ecommerce Website",
        "description": "Fully functional ecommerce website",
    },
    {
        "id": "2",
        "title": "Portfolio Website",
        "description": "A personal website to write articles and display work",
    },
    {
        "id": "3",
        "title": "Social Network",
        "description": "An open source project built by the community",
    },
]


def projects(request):
    page = "Project "
    number = 10
    rangee = [i for i in range(1, 11)]
    print(page)
    context = {
        "Page": page,
        "Number": number,
        "projectsList": projectsList,
        "range": rangee,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = None
    for i in projectsList:
        if i["id"] == str(pk):
            projectObj = i
    print("hello")
    print(projectObj)
    return render(request, "projects/single-project.html", {"projectObj": projectObj})


# Create your views here.
