from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProcessViewSet, InputViewSet, InputPriceViewSet, 
    ProcessExecutionViewSet, InputUsageViewSet, ProcessMembershipViewSet
)

router = DefaultRouter()
router.register(r'processes', ProcessViewSet)
router.register(r'inputs', InputViewSet)
router.register(r'input-prices', InputPriceViewSet)
router.register(r'executions', ProcessExecutionViewSet)
router.register(r'usages', InputUsageViewSet)
router.register(r'memberships', ProcessMembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
