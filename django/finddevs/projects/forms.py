from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project  # the class we need form for
        # fields = "__all__"  # all means it will add all the feilds for form except auto generating or non editable ones
        fields = [
            "title",
            "featured_image",
            "description",
            "demo_link",
            "source_link",
            "tags",
        ]
