# Generated by Django 5.0 on 2024-01-16 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district_wise', '0004_alter_district_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
