from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.TaskListCreateAPIView.as_view(), name="tasks"),
    path(
        "tasks/<int:id>/",
        views.TaskUpdateDeleteAPIView.as_view(),
        name="task-update-delete",
    ),
]
