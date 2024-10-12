from django.shortcuts import render
from django.shortcuts import get_object_or_404
from api.apps.models import Comic


def index(request):
    context = {}
    return render(request, "pages/index.html", context)


def digital(request):
    context = {}
    return render(request, "pages/digital.html", context)


def privacy(request):
    context = {}
    return render(request, "pages/privacy.html", context)


def terms(request):
    context = {}
    return render(request, "pages/terms.html", context)


def comic(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    context = {"comic": comic}
    return render(request, "pages/comic.html", context)
