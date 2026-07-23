## Project Overview
This is a simple task management Rest API built using Django Rest Framework. It allows users to create, read, update, and delete tasks. The API supports filtering tasks by status and priority, as well as searching tasks by title.

# Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2.  navigate to the project directory:
   ```bash
   cd task_management
   ```
3. Create a virtual environment and activate it:
   ```bash
    python -m venv .venv
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Apply migrations:
    ```bash
    python manage.py migrate
    ```
6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Endpoint Reference Summary

1. POST /api/create/task/ — Create task
This endpoint allows you to create a new task. You need to provide the task details in the request body.
- **Title**: The title of the task.
- **Status**: The status of the task (choices: Pending, InProgress, Completed) default: Pending.
- **Priority**: The priority of the task (choices: Low, Medium, High) default: Low.

sample request body:
```json
{
    "title": "Sample Task",
    "status": "Pending", #choices: Pending, InProgress, Completed
    "priority": "Low" #choices: Low, Medium, High
}
```

2. GET /api/list/tasks/ — List tasks (Supports ?status=, ?priority=, ?search=, ?ordering=)
This endpoint retrieves a list of tasks. You can filter the tasks by status and priority, search by title, and order the results.
sample request:
```
GET /api/list/tasks/?status=Pending&priority=High
```
3. GET /api/get/task/id/ — Retrieve single task
This endpoint retrieves the details of a single task by its ID.
sample request:
```
GET /api/get/task/1/
```

4. PUT /api/update/task/id/ — Full update task
This endpoint allows you to fully update an existing task by its ID. You need to provide the updated task details in the request body.
sample request body:
```json
{
    "title": "Updated Task",
    "status": "InProgress",
    "priority": "High"
}
```

5. PATCH /api/update/task/id/ — Partial update task
This endpoint allows you to partially update an existing task by its ID. You need to provide the updated task details in the request body.
sample request body:
```json
{
    "title": "Partially Updated Task"
}
```

6. DELETE /api/delete/task/id/ — Delete task
This endpoint allows you to delete a task by its ID.
sample request:
```
DELETE /api/delete/task/1/
```