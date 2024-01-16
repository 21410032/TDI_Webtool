# Generated by Django 5.0 on 2024-01-16 08:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district_wise', '0003_rename_owner_district_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='user',
            field=models.ForeignKey(default='7667605908', on_delete=django.db.models.deletion.CASCADE, related_name='districts', to=settings.AUTH_USER_MODEL),
        ),
    ]