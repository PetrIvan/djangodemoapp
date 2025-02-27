from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.list_tasks, name="tasks-list"),
]
