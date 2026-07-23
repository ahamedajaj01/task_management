from django.urls import path
from . import views

urlpatterns = [
    path('create/task/', views.CreateTaskView.as_view(), name='create_task'),
    path('list/tasks/', views.ListTasksView.as_view(), name='list_tasks'),
    path('get/task/<int:pk>/', views.GetTaskView.as_view(), name='get_task'),
    path('update/task/<int:pk>/', views.UpdateTaskView.as_view(), name='update_task'),
    path('delete/task/<int:pk>/', views.DeleteTaskView.as_view(), name='delete_task'),
]
