from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry, Lane
from datetime import date

def home(request):
    default_lanes = ["Education", "Work Experience", "Personal Projects"]

    if Lane.objects.count() == 0:
        for name in default_lanes:
            Lane.objects.create(name=name)

    if request.method == "POST":
        # ----- SETTINGS - LANE ACTIONS -----
        # Add lane if "add_lane" is in POST data
        if "add_lane" in request.POST:
            lane_name = request.POST.get("lane_name")
            if lane_name:
                Lane.objects.create(name=lane_name)
            return redirect("home")
        
        # Rename lane if "rename_lane" is in POST data
        if "rename_lane" in request.POST:
            lane_id = request.POST.get("lane_id")
            new_name = request.POST.get("new_name")
            if lane_id and new_name:
                lane = get_object_or_404(Lane, id=lane_id)
                lane.name = new_name
                lane.save()
            return redirect("home")
        
        # Delete lane if "delete_lane" is in POST data
        if "delete_lane" in request.POST:
            lane_id = request.POST.get("lane_id")
            lane = get_object_or_404(Lane, id=lane_id)
            lane.delete()
            return redirect("home")

        # ----- ENTRY ACTIONS -----
        # Delete entry if "delete" is in POST data
        if "delete" in request.POST:
            entry_id = request.POST.get("project_id")
            if entry_id:
                Entry.objects.filter(id=entry_id).delete()
            return redirect("home")

        # Read form data for creating/editing entry
        entry_id = request.POST.get("project_id")
        name = request.POST.get("name")
        lane_id = request.POST.get("lane")
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None

        # Get lane object if lane_id is provided
        lane_obj = get_object_or_404(Lane, id=lane_id)

        # Edit existing entry if entry_id is provided
        if entry_id:
            entry = get_object_or_404(Entry, id=entry_id)
            entry.name = name
            entry.lane = lane_obj
            entry.start_date = start_date
            entry.end_date = end_date
            entry.save()

        # Create new entry if no entry_id is provided
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

    lanes = Lane.objects.prefetch_related("entries")
    for lane in lanes:
        lane.sorted_entries = sorted(lane.entries.all(), key=sort_key, reverse=True)

    return render(request, "home.html", {
        "lanes": lanes
    })