from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import ServiceRequest


class ServiceRequestValidationTests(TestCase):
    def make_request(self, **overrides):
        data = {
            "title": "Synthetic laptop support request",
            "description": "Synthetic laboratory record",
            "category": ServiceRequest.Category.IT,
            "status": ServiceRequest.Status.OPEN,
            "priority": ServiceRequest.Priority.MEDIUM,
        }
        data.update(overrides)
        return ServiceRequest(**data)

    def test_resolved_without_resolved_at_fails_full_clean(self):
        request = self.make_request(
            status=ServiceRequest.Status.RESOLVED,
            resolution_summary="Issue fixed",
        )
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("resolved_at", context.exception.message_dict)

    def test_resolved_without_summary_fails_full_clean(self):
        request = self.make_request(
            status=ServiceRequest.Status.RESOLVED,
            resolved_at=timezone.now(),
        )
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("resolution_summary", context.exception.message_dict)

    def test_closed_without_required_resolution_data_fails(self):
        request = self.make_request(status=ServiceRequest.Status.CLOSED)
        with self.assertRaises(ValidationError):
            request.full_clean()

    def test_valid_resolved_request_passes_full_clean(self):
        request = self.make_request(
            status=ServiceRequest.Status.RESOLVED,
            resolved_at=timezone.now(),
            resolution_summary="Replaced the faulty cable and verified operation.",
        )
        request.full_clean()

    def test_blank_summary_is_allowed_for_open_request(self):
        request = self.make_request(status=ServiceRequest.Status.OPEN)
        request.full_clean()

    def test_due_at_is_nullable(self):
        request = self.make_request(due_at=None)
        request.full_clean()
        self.assertIsNone(request.due_at)

    def test_due_date_query_returns_only_earlier_requests(self):
        chosen_time = timezone.now()
        earlier = self.make_request(
            title="Synthetic earlier due request",
            due_at=chosen_time - timedelta(hours=1),
        )
        later = self.make_request(
            title="Synthetic later due request",
            due_at=chosen_time + timedelta(hours=1),
        )
        earlier.save()
        later.save()
        result = ServiceRequest.objects.filter(due_at__lt=chosen_time)
        self.assertEqual(list(result), [earlier])
