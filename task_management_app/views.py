from .models import Task
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import TaskSerializer


# Create Task
class CreateTaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Task created successfully",
                "task": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# List Tasks
class ListTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()

        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        priority_param = self.request.query_params.get("priority")
        if priority_param:
            queryset = queryset.filter(priority__iexact=priority_param)

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = self.request.query_params.get("ordering")
        allowed_fields = [
            "id", "-id",
            "title", "-title",
            "status", "-status",
            "priority", "-priority",
        ]

        if ordering in allowed_fields:
            queryset = queryset.order_by(ordering)

        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(
            {
                "message": "Tasks retrieved successfully",
                "tasks": serializer.data,
            }
        )


# Get Single Task
class GetTaskView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())

        return Response(
            {
                "message": "Task retrieved successfully",
                "task": serializer.data,
            }
        )


# Update Task
class UpdateTaskView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": "Task updated successfully",
                "task": serializer.data,
            }
        )


# Delete Task
class DeleteTaskView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "message": "Task deleted successfully",
            },
            status=status.HTTP_200_OK,
        )