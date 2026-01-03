from rest_framework import permissions
from .models import ProcessMembership

class IsProcessManager(permissions.BasePermission):
    """
    Allows access only to users who have 'can_manage' permission for the process.
    """
    def has_object_permission(self, request, view, obj):
        # Assumes obj is a Process or related to a Process
        if hasattr(obj, 'process'):
            process = obj.process
        elif hasattr(obj, 'execution'):
             process = obj.execution.process
        else:
            process = obj

        return ProcessMembership.objects.filter(
            user=request.user, 
            process=process, 
            can_manage=True
        ).exists()

class CanExecuteProcess(permissions.BasePermission):
    """
    Allows access to users who have 'can_execute' permission for the process.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'process'):
            process = obj.process
        else:
            process = obj
            
        return ProcessMembership.objects.filter(
            user=request.user,
            process=process,
            can_execute=True
        ).exists()
