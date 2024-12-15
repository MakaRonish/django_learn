from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProjects(request):
    search_query = ""
    if request.GET.get("text"):
        search_query = request.GET.get("text")

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(owner__name__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(tags__name__icontains=search_query)
    )
    return projects, search_query


def paginateProjects(request, projects, result):
    page = request.GET.get("page")  # query string

    paginator = Paginator(projects, result)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # gives the number of page
        projects = paginator.page(page)

    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex + 1)

    return projects, custom_range, paginator
