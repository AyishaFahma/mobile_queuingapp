# Generated by Django 4.0.1 on 2024-04-14 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_bussiness_chat_from_rename_customer_chat_to'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='meassage',
            new_name='message',
        ),
    ]
