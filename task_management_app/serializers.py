from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200, required=False, allow_blank=False)
    status = serializers.ChoiceField(choices=Task.Status.choices, required=False)
    priority = serializers.ChoiceField(choices=Task.Priority.choices, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority'] 

    def validate_title(self, value):
        if value is not None:
            if not value.strip():
                raise serializers.ValidationError("Title cannot be empty or whitespace only.")
        return value

    def validate_status(self, value):
        if value is not None:
            valid_statuses = [choice[0] for choice in Task.Status.choices]
            if value not in valid_statuses:
                raise serializers.ValidationError(
                    f"Invalid status '{value}'. Allowed values are: {', '.join(valid_statuses)}."
                )
        return value

    def validate_priority(self, value):
        if value is not None:
            valid_priorities = [choice[0] for choice in Task.Priority.choices]
            if value not in valid_priorities:
                raise serializers.ValidationError(
                    f"Invalid priority '{value}'. Allowed values are: {', '.join(valid_priorities)}."
                )
        return value

    def create(self, validated_data):
        if not validated_data.get('title') or not validated_data.get('title').strip():
            raise serializers.ValidationError({'title': ['Title is required to create a task.']})
        if 'status' not in validated_data:
            validated_data['status'] = Task.Status.PENDING
        if 'priority' not in validated_data:
            validated_data['priority'] = Task.Priority.LOW
        return super().create(validated_data)





    