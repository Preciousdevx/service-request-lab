from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from requests_app.models import ServiceRequest


class Command(BaseCommand):
    help = "Create synthetic service requests for the laboratory exercise."

    def handle(self, *args, **options):
        ServiceRequest.objects.all().delete()
        now = timezone.now()
        rows = [
            ("Synthetic Wi-Fi fault 01", "IT", "OPEN", 4),
            ("Synthetic printer fault 02", "IT", "ASSIGNED", 3),
            ("Synthetic account access 03", "IT", "OPEN", 2),
            ("Synthetic software setup 04", "IT", "RESOLVED", 1),
            ("Synthetic network check 05", "IT", "CLOSED", 3),
            ("Synthetic email issue 06", "IT", "ASSIGNED", 2),
            ("Synthetic leaking tap 07", "MAINT", "OPEN", 4),
            ("Synthetic lighting fault 08", "MAINT", "ASSIGNED", 3),
            ("Synthetic door repair 09", "MAINT", "RESOLVED", 2),
            ("Synthetic plumbing check 10", "MAINT", "CLOSED", 1),
            ("Synthetic furniture repair 11", "MAINT", "OPEN", 2),
            ("Synthetic power issue 12", "MAINT", "ASSIGNED", 4),
        ]
        for i, (title, category, status, priority) in enumerate(rows):
            resolved = status in ("RESOLVED", "CLOSED")
            ServiceRequest.objects.create(
                title=title,
                description="Synthetic data created only for the class laboratory exercise.",
                category=category,
                status=status,
                priority=priority,
                created_at=now - timedelta(days=i),
                due_at=now + timedelta(hours=i - 5),
                resolved_at=(now - timedelta(hours=i)) if resolved else None,
                resolution_summary=("Synthetic resolution completed and verified." if resolved else ""),
            )
        self.stdout.write(self.style.SUCCESS("Created 12 synthetic service requests."))
