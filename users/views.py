from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UsersSerializer, UserCreateSerializer

# Class based view to handle GET requests for a list of users
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    # Function to handle GET requests
    def get(self, request, *args, **kwargs):
        # Retrieve all users from the database
        users = CustomUser.objects.all()

        # Serialize the users data using the UserSerializer
        serializer = UsersSerializer(users, many=True)

        # Return a response object with the serialized data
        return Response(serializer.data)
    

# Class based view to handle POST requests for creating new users
class UserCreateAPIView(APIView):
    # function method to handle POST requests
    def post(self, request, *args, **kwargs):
        # new UserSerializer instance with the request data
        serializer = UserCreateSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the serializer data to the database
            user = serializer.save()

            # Set the password for the user
            user.set_password(user.password)
            user.save()

            # Return a response object with the serialized data and a 201 Created status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the serializer is not valid, return a Response object withthe error messages and a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)