from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission class that checks if the user is the owner of a task
class IsTaskOwner(BasePermission):
    # Method that checks if the user has permission to access a specific object
    def has_object_permission(self, request,view, obj):
        # Check if the method is safe , allow access to the object 
        if request.method in SAFE_METHODS:
            return True
        # If the metho is not safe , check if the user is the owner by
        # comparing the user attribute of the object to the requests user attribute
        return obj.user == request.user