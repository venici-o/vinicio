from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import build_dashboard_context


@login_required
def dashboard_home(request):
    context = build_dashboard_context(request.user)
    return render(request, "dashboard/index.html", context)
