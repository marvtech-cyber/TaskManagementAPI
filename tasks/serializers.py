from rest_framework import serializers
from .models import Task
import datetime

# Define serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    # Define metadata for the serializer
    class Meta:
        # Model used by the serializer
        model = Task
        # Model fields that will be included in the serialized representation
        fields = ['id', 'title', 'description', 'due_date', 'priority_level', 'status', 'completed_at', 'created_at', 'updated_at']

    # Custom validation method for the due_date field
    def validate_due_date(self, value):
        # Check if the due_date is in the past
        if value < datetime.date.today():

            # if the due_date is in the past, raise a ValidationError
            raise serializers.ValidationError('Due date must be in the future')
        # If due_date is valid, return the original value 
        return value
    
    # Custom validation method for the status field
    def validate_status(self, value):
        # Check if the status is being set to 'Completed' an if the task is already completed
        if value == 'Completed' and self.instance and self.instance.status == 'Completed':
            # If the task is already completed, raise a ValidationError
            raise serializers.ValidationError('Task is already completed')
        # If the status is valid, return the original value
        return value