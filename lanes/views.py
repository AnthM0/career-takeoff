from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from datetime import date

def home(request):
    if request.method == "POST":
        # DELETE
        if "delete" in request.POST:
            project_id = request.POST.get("project_id")
            Project.objects.filter(id=project_id).delete()
            return redirect("home")

        project_id = request.POST.get("project_id")
        name = request.POST.get("name")
        lane = request.POST.get("lane")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if project_id:  # EDIT
            project = get_object_or_404(Project, id=project_id)
            project.name = name
            project.start_date = start_date or None
            project.end_date = end_date or None
            project.save()
        else:  # CREATE
            if name and lane:
                Project.objects.create(
                    name=name,
                    lane=lane,
                    start_date=start_date or None,
                    end_date=end_date or None
                )

        return redirect("home")

    def sort_key(p):
        # Treat "present" as far future so it sorts last
        end = p.end_date if p.end_date and p.end_date != "present" else "9999-12"
        start = p.start_date if p.start_date else "0000-00"
        return (end, start)

    projects = sorted(Project.objects.all(), key=sort_key, reverse=True)

    lanes = [
        (1, "Education"),
        (2, "Work Experience"),
        (3, "Personal Projects"),
    ]

    return render(request, "home.html", {
        "projects": projects,
        "lanes": lanes
    })