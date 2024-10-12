from django.urls import path

from api.apps.api import comic_views as views

app_name = "api_comics"

urlpatterns = [
    path("comics/", view=views.comic_list, name="comics"),
    path("comics/<int:pk>/", view=views.comic_detail, name="comic_detail"),
]
