from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Process, ProcessStep, Input, InputPrice, ProcessExecution, InputUsage, ProcessMembership
from datetime import timedelta

class CostCalculationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.process = Process.objects.create(name='Test Process')
        self.input = Input.objects.create(name='Corn', default_unit='kg')
        
        # Create price history
        now = timezone.now()
        self.price1 = InputPrice.objects.create(
            input=self.input,
            price=100.00,
            valid_from=now - timedelta(days=10),
            valid_to=now - timedelta(days=5)
        )
        self.price2 = InputPrice.objects.create(
            input=self.input,
            price=120.00,
            valid_from=now - timedelta(days=5),
            valid_to=None # Current price
        )

    def test_execution_exchange_rate_snapshot(self):
        execution = ProcessExecution.objects.create(
            process=self.process,
            user=self.user
        )
        self.assertIsNotNone(execution.exchange_rate_snapshot)
        self.assertEqual(execution.exchange_rate_snapshot, 1000.00) # Dummy value

    def test_input_usage_cost_calculation_current_price(self):
        execution = ProcessExecution.objects.create(
            process=self.process,
            user=self.user
        )
        usage = InputUsage.objects.create(
            execution=execution,
            input=self.input,
            quantity=10
        )
        
        from decimal import Decimal
        self.assertEqual(usage.price_snapshot_ars, Decimal('120.00'))
        self.assertEqual(usage.total_cost_ars, Decimal('1200.00'))
        self.assertEqual(usage.total_cost_usd, Decimal('1.20')) # 1200 / 1000

    def test_input_usage_cost_calculation_historic_price(self):
        # Create execution in the past
        past_time = timezone.now() - timedelta(days=7)
        execution = ProcessExecution.objects.create(
            process=self.process,
            user=self.user
        )
        # Manually set timestamp to past (auto_now_add might override if not careful, but default=timezone.now lets us override)
        execution.timestamp = past_time
        execution.save()
        
        usage = InputUsage.objects.create(
            execution=execution,
            input=self.input,
            quantity=10
        )
        
        from decimal import Decimal
        self.assertEqual(usage.price_snapshot_ars, Decimal('100.00'))
        self.assertEqual(usage.total_cost_ars, Decimal('1000.00'))
        self.assertEqual(usage.total_cost_usd, Decimal('1.00')) # 1000 / 1000

    def test_missing_price_raises_error(self):
        # Execution way in the past before any price
        past_time = timezone.now() - timedelta(days=20)
        execution = ProcessExecution.objects.create(
            process=self.process,
            user=self.user
        )
        execution.timestamp = past_time
        execution.save()
        
        with self.assertRaises(Exception): # ValidationError
            InputUsage.objects.create(
                execution=execution,
                input=self.input,
                quantity=10
            )

class APITests(TestCase):
    def test_schema_generation(self):
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('openapi' in response.content.decode('utf-8') or 'swagger' in response.content.decode('utf-8'))

