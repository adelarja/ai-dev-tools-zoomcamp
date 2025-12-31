from rest_framework import viewsets, permissions
from .models import Process, Input, InputPrice, ProcessExecution, InputUsage, ProcessMembership
from .serializers import (
    ProcessSerializer, InputSerializer, InputPriceSerializer, 
    ProcessExecutionSerializer, InputUsageSerializer, ProcessMembershipSerializer
)
from .permissions import IsProcessManager, CanExecuteProcess

class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [permissions.IsAuthenticated] # Add IsProcessManager for write operations if needed

class InputViewSet(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]

class InputPriceViewSet(viewsets.ModelViewSet):
    queryset = InputPrice.objects.all()
    serializer_class = InputPriceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProcessExecutionViewSet(viewsets.ModelViewSet):
    queryset = ProcessExecution.objects.all()
    serializer_class = ProcessExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InputUsageViewSet(viewsets.ModelViewSet):
    queryset = InputUsage.objects.all()
    serializer_class = InputUsageSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProcessMembershipViewSet(viewsets.ModelViewSet):
    queryset = ProcessMembership.objects.all()
    serializer_class = ProcessMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
