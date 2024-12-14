from .models import Project, Tag
from django.db.models import Q


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
