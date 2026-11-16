from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="ServiceRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("category", models.CharField(choices=[("IT", "IT Support"), ("MAINT", "Maintenance")], max_length=10)),
                ("status", models.CharField(choices=[("OPEN", "Open"), ("ASSIGNED", "Assigned"), ("RESOLVED", "Resolved"), ("CLOSED", "Closed")], default="OPEN", max_length=10)),
                ("priority", models.PositiveSmallIntegerField(choices=[(1, "Low"), (2, "Medium"), (3, "High"), (4, "Urgent")], default=2)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
