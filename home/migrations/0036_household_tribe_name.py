# Generated by Django 4.2.4 on 2023-11-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_tribe_image_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='tribe_name',
            field=models.CharField(default='Not specified', max_length=30),
            preserve_default=False,
        ),
    ]
