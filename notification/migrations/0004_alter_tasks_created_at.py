# Generated by Django 4.2.16 on 2024-11-26 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_alter_notification_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
