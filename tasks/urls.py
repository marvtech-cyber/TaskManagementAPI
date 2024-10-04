from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView,TaskCompleteAPIView, TaskCreateAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view()),
    path('tasks/create', TaskCreateAPIView.as_view()),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view()),
    path('tasks/<int:task_id>/complete/', TaskCompleteAPIView.as_view())
]