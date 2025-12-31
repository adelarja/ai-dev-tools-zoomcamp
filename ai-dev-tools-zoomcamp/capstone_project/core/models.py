from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Process(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ProcessStep(models.Model):
    process = models.ForeignKey(Process, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.process.name} - {self.name}"

class Input(models.Model):
    name = models.CharField(max_length=255)
    default_unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class InputPrice(models.Model):
    input = models.ForeignKey(Input, related_name='prices', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ARS
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.input.name} - ${self.price} ({self.valid_from})"

class ProcessMembership(models.Model):
    user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    process = models.ForeignKey(Process, related_name='memberships', on_delete=models.CASCADE)
    can_execute = models.BooleanField(default=False)
    can_view_metrics = models.BooleanField(default=False)
    can_manage = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'process')

    def __str__(self):
        return f"{self.user.username} - {self.process.name}"

class ProcessExecution(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
    ]

    process = models.ForeignKey(Process, related_name='executions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='executions', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    exchange_rate_snapshot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # USD/ARS

    def save(self, *args, **kwargs):
        if not self.exchange_rate_snapshot:
            # TODO: Fetch real exchange rate. For now using a dummy value.
            from decimal import Decimal
            self.exchange_rate_snapshot = Decimal('1000.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.process.name} - {self.user.username} - {self.timestamp}"

class InputUsage(models.Model):
    execution = models.ForeignKey(ProcessExecution, related_name='usages', on_delete=models.CASCADE)
    input = models.ForeignKey(Input, related_name='usages', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_snapshot_ars = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost_ars = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_cost_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price_snapshot_ars:
            # Find the price valid at execution time
            price_obj = self.input.prices.filter(
                valid_from__lte=self.execution.timestamp
            ).filter(
                models.Q(valid_to__gte=self.execution.timestamp) | models.Q(valid_to__isnull=True)
            ).order_by('-valid_from').first()

            if price_obj:
                self.price_snapshot_ars = price_obj.price
            else:
                # Handle missing price. For now, raise error or set to 0.
                # Raising error is safer for data integrity.
                raise ValidationError(f"No valid price found for input {self.input.name} at {self.execution.timestamp}")

        if self.price_snapshot_ars and self.quantity:
            self.total_cost_ars = self.price_snapshot_ars * self.quantity
            if self.execution.exchange_rate_snapshot:
                self.total_cost_usd = self.total_cost_ars / self.execution.exchange_rate_snapshot

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.execution} - {self.input.name}: {self.quantity}"
