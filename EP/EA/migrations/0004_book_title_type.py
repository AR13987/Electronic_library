# Generated by Django 5.1.3 on 2024-11-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EA', '0003_publisher_edition'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='title_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
