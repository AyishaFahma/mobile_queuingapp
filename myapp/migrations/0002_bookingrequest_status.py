# Generated by Django 5.0.2 on 2024-03-23 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingrequest',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]
