# Generated by Django 4.2.6 on 2023-12-01 19:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("general", "0003_remove_sitedetail_unique_site_detail_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="sitedetail",
            name="unique_site_detail",
        ),
        migrations.AddConstraint(
            model_name="sitedetail",
            constraint=models.CheckConstraint(
                check=models.Q(("id__isnull", False)), name="unique_site_detail"
            ),
        ),
    ]