from django.test import TestCase
from .models import PressureReading, PressureSensor
from django.utils.dateparse import parse_datetime
from django.urls import reverse

class AggregationAPITestCase(TestCase):

    def setUp(self):
        sensor = PressureSensor.objects.create(
            label='PSSR-TestSensor',
            latitude=0.0,
            longitude=0.0
        )
        PressureReading.objects.create(value=10, datetime=parse_datetime('2024-08-01T10:00:00Z'), sensor=sensor)
        PressureReading.objects.create(value=20, datetime=parse_datetime('2024-08-02T10:00:00Z'), sensor=sensor)
        PressureReading.objects.create(value=30, datetime=parse_datetime('2024-08-03T10:00:00Z'), sensor=sensor)

    def test_until_after_since(self):
        response = self.client.get(reverse('aggregate'), {
            'since': '2024-08-03T00:00:00Z',
            'until': '2024-08-01T23:59:59Z',
            'calculation': 'sum'
        })
        self.assertEqual(response.status_code, 400)
    def test_retrieve_readings_within_time_period(self):
        response = self.client.get(reverse('aggregate'), {
            'since': '2024-08-01T00:00:00Z',
            'until': '2024-08-02T23:59:59Z',
            'calculation': 'sum'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 30)  # 10 + 20

    def test_sum_calculation(self):
        response = self.client.get(reverse('aggregate'), {
            'since': '2024-08-01T00:00:00Z',
            'until': '2024-08-03T23:59:59Z',
            'calculation': 'sum'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 60)  # 10 + 20 + 30

    def test_avg_calculation(self):
        response = self.client.get(reverse('aggregate'), {
            'since': '2024-08-01T00:00:00Z',
            'until': '2024-08-03T23:59:59Z',
            'calculation': 'avg'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 20)  # (10 + 20 + 30) / 3

    def test_no_readings_within_time_period(self):
        response = self.client.get(reverse('aggregate'), {
            'since': '2025-08-01T00:00:00Z',
            'until': '2025-08-03T23:59:59Z',
            'calculation': 'sum'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 0)

    def test_missing_query_parameters(self):
        response = self.client.get(reverse('aggregate'), {
            'since': '2024-08-01T00:00:00Z',
            'until': '2024-08-02T23:59:59Z',
        })
        self.assertEqual(response.status_code, 400)

   
