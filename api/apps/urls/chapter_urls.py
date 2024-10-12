from django.urls import path

from api.apps.api import chapter_views as views

app_name = "api_chapters"

urlpatterns = [
    path("chapters/", view=views.chapter_list, name="chapters"),
    path("chapters/<int:pk>/", view=views.chapter_detail, name="chapter_detail"),
]
