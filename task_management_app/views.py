from .models import Task
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import TaskSerializer

# create task
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
                "id": serializer.instance.id,
                "task": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

# list tasks with optional filtering by status, priority, and search by title
class ListTasksView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        priority_param = self.request.query_params.get('priority')
        if priority_param:
            queryset = queryset.filter(priority__iexact=priority_param)

        search_param = self.request.query_params.get('search') or self.request.query_params.get('title')
        if search_param:
            queryset = queryset.filter(title__icontains=search_param)

        ordering = self.request.query_params.get('ordering') or self.request.query_params.get('sort_by')
        if ordering:
            order_param = self.request.query_params.get('order') or self.request.query_params.get('sort_order')
            if order_param and order_param.lower() == 'desc' and not ordering.startswith('-'):
                ordering = f'-{ordering}'

            allowed_fields = ['id', '-id', 'title', '-title', 'status', '-status', 'priority', '-priority']
            if ordering in allowed_fields:
                queryset = queryset.order_by(ordering)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "message": "Tasks retrieved successfully",
                "tasks": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# update task by id using PUT or PATCH method
class UpdateTaskView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            {
                "message": "Task updated successfully",
                "id": instance.id,
                "task": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# get single task by id
class GetTaskView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(
            {
                "message": "Task retrieved successfully",
                "id": instance.id,
                "task": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# delete task by id
class DeleteTaskView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "message": "Task deleted successfully",
                "id": instance.id,
            },
            status=status.HTTP_200_OK,
        )
