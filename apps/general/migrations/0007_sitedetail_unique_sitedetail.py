# Generated by Django 4.2.6 on 2024-01-08 19:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("general", "0006_alter_message_options"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="sitedetail",
            constraint=models.UniqueConstraint(
                condition=models.Q(("id__isnull", True)),
                fields=("id",),
                name="unique_sitedetail",
            ),
        ),
    ]
