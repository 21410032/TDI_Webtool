# Generated by Django 4.2.4 on 2024-01-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0048_user_hitcounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_hitcounts',
            name='site_views',
            field=models.IntegerField(default=0),
        ),
    ]
