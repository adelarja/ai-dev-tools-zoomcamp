from rest_framework import serializers
from .models import Process, ProcessStep, Input, InputPrice, ProcessExecution, InputUsage, ProcessMembership

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = ['id', 'name', 'order']

class ProcessSerializer(serializers.ModelSerializer):
    steps = ProcessStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Process
        fields = ['id', 'name', 'description', 'steps']

class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ['id', 'name', 'default_unit']

class InputPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputPrice
        fields = ['id', 'input', 'price', 'valid_from', 'valid_to', 'source']

class InputUsageSerializer(serializers.ModelSerializer):
    input_name = serializers.CharField(source='input.name', read_only=True)
    
    class Meta:
        model = InputUsage
        fields = ['id', 'execution', 'input', 'input_name', 'quantity', 'price_snapshot_ars', 'total_cost_ars', 'total_cost_usd']
        read_only_fields = ['price_snapshot_ars', 'total_cost_ars', 'total_cost_usd']

class ProcessExecutionSerializer(serializers.ModelSerializer):
    usages = InputUsageSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    process_name = serializers.CharField(source='process.name', read_only=True)
    
    class Meta:
        model = ProcessExecution
        fields = ['id', 'process', 'process_name', 'user', 'user_username', 'timestamp', 'notes', 'status', 'exchange_rate_snapshot', 'usages']
        read_only_fields = ['exchange_rate_snapshot', 'timestamp']

class ProcessMembershipSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    process_name = serializers.CharField(source='process.name', read_only=True)

    class Meta:
        model = ProcessMembership
        fields = ['id', 'user', 'user_username', 'process', 'process_name', 'can_execute', 'can_view_metrics', 'can_manage']
