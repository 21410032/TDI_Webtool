# Generated by Django 4.2.4 on 2024-01-18 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0044_alter_household_arts_score_alter_household_ass_score_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='user',
        ),
        migrations.RemoveField(
            model_name='household',
            name='year',
        ),
        migrations.AddField(
            model_name='tribe',
            name='user',
            field=models.ForeignKey(default='7219142469', on_delete=django.db.models.deletion.CASCADE, related_name='households', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tribe',
            name='year',
            field=models.IntegerField(default=2022),
            preserve_default=False,
        ),
    ]
