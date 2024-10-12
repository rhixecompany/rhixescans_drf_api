from django.urls import path

from api.apps.api import user_views as views

app_name = "api_users"

urlpatterns = [
    path("users/", view=views.user_list, name="users"),
    path("users/<int:pk>/", view=views.user_detail, name="user_detail"),
]
