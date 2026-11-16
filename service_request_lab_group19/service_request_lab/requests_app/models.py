from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ServiceRequest(models.Model):
    class Category(models.TextChoices):
        IT = "IT", "IT Support"
        MAINTENANCE = "MAINT", "Maintenance"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        ASSIGNED = "ASSIGNED", "Assigned"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        URGENT = 4, "Urgent"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=10, choices=Category.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # Extension fields (introduced by migration 0002).
    due_at = models.DateTimeField(null=True, blank=True)
    resolution_summary = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "due_at"], name="status_due_idx"),
        ]

    def clean(self):
        super().clean()
        errors = {}
        if self.status in (self.Status.RESOLVED, self.Status.CLOSED):
            if not self.resolved_at:
                errors["resolved_at"] = "Resolved or closed requests must have a resolved_at timestamp."
            if not self.resolution_summary or not self.resolution_summary.strip():
                errors["resolution_summary"] = "Resolved or closed requests must include a resolution summary."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
