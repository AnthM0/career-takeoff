from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry, Lane
from datetime import date

def home(request):
    if request.method == "POST":
        # ----- DELETE ----- 
        if "delete" in request.POST:
            entry_id = request.POST.get("project_id")
            if entry_id:
                Entry.objects.filter(id=entry_id).delete()
            return redirect("home")

        # ----- READ FORM DATA -----
        entry_id = request.POST.get("project_id")
        name = request.POST.get("name")
        lane_id = request.POST.get("lane")
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None

        # ----- GET LANE OBJECT -----
        lane_obj = None
        if lane_id:
            lane_obj = get_object_or_404(Lane, id=lane_id)

        # ----- EDIT EXISTING ENTRY -----
        if entry_id:
            entry = get_object_or_404(Entry, id=entry_id)
            entry.name = name
            entry.lane = lane_obj
            entry.start_date = start_date
            entry.end_date = end_date
            entry.save()

        # ----- CREATE NEW ENTRY -----
        else:
            if name and lane_obj:
                Entry.objects.create(
                    name=name,
                    lane=lane_obj,
                    start_date=start_date,
                    end_date=end_date
                )

        return redirect("home")

    def sort_key(entry):
        # Treat "present" as far future so it sorts last
        end = entry.end_date if entry.end_date and entry.end_date != "Present" else "9999-12"
        start = entry.start_date if entry.start_date else "0000-00"
        return (end, start)

    default_lanes = [
        "Education",
        "Work Experience",
        "Personal Projects",
    ]
    for name in default_lanes:
        Lane.objects.get_or_create(name=name)

    lanes = Lane.objects.prefetch_related("entries")
    for lane in lanes:
        lane.sorted_entries = sorted(lane.entries.all(), key=sort_key, reverse=True)

    return render(request, "home.html", {
        "lanes": lanes
    })