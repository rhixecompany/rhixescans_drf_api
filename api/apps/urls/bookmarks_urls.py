from django.urls import path

from api.apps.views import bookmarks_views as views

app_name = "bookmarks"

urlpatterns = [
    path("", views.BookmarkList.as_view(), name="list"),
    path("add-comic-bookmark/", views.add_comic_bookmark, name="add-comic-bookmark"),
    path(
        "remove-comic-bookmark/",
        views.remove_comic_bookmark,
        name="remove-comic-bookmark",
    ),
    path("<int:pk>/count", views.count, name="count"),
]
