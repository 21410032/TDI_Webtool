# Generated by Django 4.2.4 on 2024-01-13 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('district_wise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='user',
            field=models.ForeignKey(default='7219142469', on_delete=django.db.models.deletion.CASCADE, related_name='districts', to=settings.AUTH_USER_MODEL),
        ),
    ]