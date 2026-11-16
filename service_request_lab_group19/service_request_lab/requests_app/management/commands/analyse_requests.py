from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from requests_app.models import ServiceRequest


class Command(BaseCommand):
    help = "Print due-date results, SQL, and the database execution plan."

    def handle(self, *args, **options):
        chosen_time = timezone.now()
        due_before = ServiceRequest.objects.filter(due_at__lt=chosen_time).order_by("due_at")
        self.stdout.write(f"\nRequests due before {chosen_time.isoformat()}:")
        for request in due_before:
            self.stdout.write(f"- {request.title}: {request.due_at}")

        queryset = ServiceRequest.objects.filter(
            category=ServiceRequest.Category.IT,
            status__in=[ServiceRequest.Status.OPEN, ServiceRequest.Status.ASSIGNED],
        ).order_by("priority", "created_at")

        self.stdout.write("\nQueryset SQL:")
        self.stdout.write(str(queryset.query))
        self.stdout.write("\nQueryset EXPLAIN:")
        try:
            self.stdout.write(queryset.explain())
        except Exception as exc:
            self.stderr.write(f"Could not obtain EXPLAIN output: {exc}")
            raise
        self.stdout.write(f"\nRows returned: {queryset.count()}")
        self.stdout.write(
            "\nIndex note: inspect the actual plan above. For a tiny synthetic table, "
            "MySQL may prefer a table scan because it is cheaper than an index lookup."
        )
