from django.contrib import admin
from django.utils import timezone
from .models import ServiceRequest


class OverdueFilter(admin.SimpleListFilter):
    title = "due status"
    parameter_name = "overdue"

    def lookups(self, request, model_admin):
        return (("yes", "Overdue"), ("no", "Not overdue"))

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "yes":
            return queryset.filter(due_at__lt=now, due_at__isnull=False).exclude(
                status__in=[ServiceRequest.Status.RESOLVED, ServiceRequest.Status.CLOSED]
            )
        if self.value() == "no":
            return queryset.filter(due_at__gte=now)
        return queryset


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "priority", "created_at", "due_at", "resolved_at")
    list_filter = ("category", "status", "priority", OverdueFilter)
    search_fields = ("title", "description", "resolution_summary")
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Request", {"fields": ("title", "description", "category", "status", "priority")}),
        ("Service level", {"fields": ("created_at", "due_at")}),
        ("Resolution", {"fields": ("resolved_at", "resolution_summary")}),
    )
