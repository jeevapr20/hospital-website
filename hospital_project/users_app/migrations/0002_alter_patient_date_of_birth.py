# Generated by Django 5.1.6 on 2025-03-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
