# Generated by Django 4.2.17 on 2025-01-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jpllabcaszipperdata", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="archiver",
            name="solr_url",
            field=models.URLField(
                default="https://localhost:8984",
                help_text="Base URL to the Solr server",
            ),
        ),
    ]
