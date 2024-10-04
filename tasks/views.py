from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskOwner
import datetime

#  Class based view for creating new tasks
class TaskCreateAPIView(APIView):
    # Specify serializer and permission classes to use for this view
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwner]

    # Method to handle POST requests
    def post(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'You must be authenticated to create a task'}, status=status.HTTP_401_UNAUTHORIZED)
        # Create a serializer instance with the request data
        serializer = self.serializer_class(data=request.data)
        # Check if serializer is valid
        if serializer.is_valid():
            # Save the serializer data and set the user to the current user
            serializer.save(user=self.request.user)
            # Return a response with the serialized data and a 201 status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the serializer is not valid , return a response with the error data and 400 status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Class based view for listing all tasks
class TaskListAPIView(ListAPIView):
    # Specify the serializer and permision classes to be used for this view
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwner]

    # Method to get queryset for this view
    def get_queryset(self):
        # Return a queryset of tasks that belong to the current user
        return Task.objects.filter(user=self.request.user)

    # Method to handle GET requests
    def get(self, request, *args, **kwargs):
        # get queryset for this view
        tasks = self.get_queryset()
        # Create a serializer instance with the queryset
        serializer = self.get_serializer(tasks, many=True)
        # Return a response with the serialized data
        return Response(serializer.data)

# Class based view for retrieving, updating and deleting tasks
class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    # Specify the serializer and permission classesto be used for this view
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwner]
    # lookup field used for this view
    lookup_field = 'id'

    # Method to get the queryset for this view
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # Method to handle PUT requests
    def put(self, request, *args, **kwargs):
        # Get the task instance for this view
        instance = self.get_object()
        # Check if the task is already completed
        if instance.status == 'Completed':
            # If the task is already completed, return a response with an error message and a 400 status code
            return Response({'error': 'Task is already completed'}, status=status.HTTP_400_BAD_REQUEST)
        # Create a serializer instance with the request data
        serializer = self.get_serializer(instance, data=request.data)
        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the serialized data
            serializer.save()
            # Return a response with the serialized data
            return Response(serializer.data)
        # If the serializer is not valid, return response with the error data and 400 status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Method to handle DELETE requests
    def delete(self, request, *args, **kwargs):
        # Retrieve task instance for this view
        instance = self.get_object()
        # Check if the task is already completed, if task is completed return error message and a 400 status code in the response
        if instance.status == 'Completed':
            return Response({'error': 'Task is already completed'}, status=status.HTTP_400_BAD_REQUEST)
        # Delete the task instance an return a 204 status code
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# Class based view for completing tasks
class TaskCompleteAPIView(APIView):
    # permission classes used in this view
    permission_classes = [IsTaskOwner]

    # Method to handle POST request
    def post(self, request, *args, **kwargs):
        # Get the task ID from the URL parameters
        task_id = kwargs.get('task_id')
        # Get the task instance with the given ID
        task = Task.objects.get(id=task_id)
        # Check if the task belongs to the current user, if not return error and 403 status code in response
        if task.user != request.user:
            return Response({'error': 'You do not have permission to complete this task'}, status=status.HTTP_403_FORBIDDEN)

        # Set the task status to 'Completed' and the completed at date to the current date and time
        task.status = 'Completed'
        task.completed_at = datetime.datetime.now()
        # Save the task instance
        task.save()
        return Response({'message': 'Task completed successfully'})