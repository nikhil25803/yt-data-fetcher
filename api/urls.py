from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.load_data, name="query-api"),
    path("videos", views.get_all_videos, name="videos-data"),
    path("key/add", views.add_new_key, name="add-key"),
]
