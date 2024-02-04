# Generated by Django 4.2.4 on 2024-02-04 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_tribe_unique_together_remove_tribe_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tribe_image',
            name='tribe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tribe_image', to='home.tribe'),
        ),
    ]