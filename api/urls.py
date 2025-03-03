from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.TaskListCreateAPIView.as_view(), name="tasks"),
    path(
        "tasks/<int:id>/",
        views.TaskUpdateDeleteAPIView.as_view(),
        name="task-update-delete",
    ),
    path(
        "tasks/nearest-deadline/",
        views.TaskNearestDeadlineAPIView.as_view(),
        name="task-nearest-deadline",
    ),
    path(
        "leetcode/rotate-array",
        views.RotateArrayAPIView.as_view(),
        name="rotate-array",
    ),
    path(
        "leetcode/kth-largest",
        views.KthLargestAPIView.as_view(),
        name="kth-largest",
    ),
    path(
        "leetcode/longest-increasing-path",
        views.LongestIncreasingPathAPIView.as_view(),
        name="longest-increasing-path",
    ),
]
