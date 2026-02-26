from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Entry, Lane

# Login view
def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
    return redirect("home")

# Logout view
def logout_view(request):
    logout(request)
    return redirect("home")

# Registration view
def register_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if username and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)

    return redirect("home")

def home(request):
    return render(request, "home.html")

# Resume Engine view to display lanes and entries
def resume_engine(request):
    # Use a logged in user if available, otherwise use a default "Guest" user
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.get(username="Guest")

    # Only create default lanes if user has none
    if Lane.objects.filter(user=current_user).count() == 0:
        default_lanes = ["Education", "Work Experience", "Personal Projects"]
        for name in default_lanes:
            Lane.objects.create(user=current_user, name=name)

    if request.method == "POST":
        # ----- SETTINGS - LANE ACTIONS -----
        # Add lane if "add_lane" is in POST data
        if "add_lane" in request.POST:
            lane_name = request.POST.get("lane_name")
            if lane_name:
                Lane.objects.create(user=current_user, name=lane_name)
            return redirect("resume_engine")
        
        # Rename lane if "rename_lane" is in POST data
        if "rename_lane" in request.POST:
            lane_id = request.POST.get("lane_id")
            new_name = request.POST.get("new_name")
            if lane_id and new_name:
                lane = get_object_or_404(Lane, id=lane_id, user=current_user)
                lane.name = new_name
                lane.save()
            return redirect("resume_engine")
        
        # Delete lane if "delete_lane" is in POST data
        if "delete_lane" in request.POST:
            lane_id = request.POST.get("lane_id")
            lane = get_object_or_404(Lane, id=lane_id, user=current_user)
            lane.delete()
            return redirect("resume_engine")

        # ----- ENTRY ACTIONS -----
        # Delete entry if "delete" is in POST data
        if "delete" in request.POST:
            entry_id = request.POST.get("project_id")
            if entry_id:
                Entry.objects.filter(id=entry_id, user=current_user).delete()
            return redirect("resume_engine")

        # Read form data for creating/editing entry
        entry_id = request.POST.get("project_id")
        name = request.POST.get("name")
        lane_id = request.POST.get("lane")
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None

        # Get lane object
        lane_obj = get_object_or_404(Lane, id=lane_id, user=current_user)

        # Edit existing entry if entry_id is provided
        if entry_id:
            entry = get_object_or_404(Entry, id=entry_id, user=current_user)
            entry.name = name
            entry.lane = lane_obj
            entry.update_detail("start_date", start_date)
            entry.update_detail("end_date", end_date)
            entry.save()

        # Create new entry if no entry_id is provided
        else:
            if name and lane_obj:
                Entry.objects.create(
                    user=current_user,
                    name=name,
                    lane=lane_obj,
                    details={"start_date": start_date, "end_date": end_date}
                )

        return redirect("resume_engine")

    def sort_key(entry):
        # Treat "present" as far future so it sorts last
        end = entry.get_detail("end_date") if entry.get_detail("end_date") and entry.get_detail("end_date") != "Present" else "9999-12"
        start = entry.get_detail("start_date") if entry.get_detail("start_date") else "0000-00"
        return (end, start)

    lanes = Lane.objects.filter(user=current_user).prefetch_related("entries")
    for lane in lanes:
        lane.sorted_entries = sorted(lane.entries.all(), key=sort_key, reverse=True)

    return render(request, "resumeEngine.html", {
        "lanes": lanes,
        "current_user": current_user
    })