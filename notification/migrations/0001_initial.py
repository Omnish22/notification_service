# Generated by Django 4.2.16 on 2024-11-20 14:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('email', 'Email'), ('sms', 'Sms'), ('push', 'Push')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')], max_length=20)),
                ('content', models.JSONField(blank=True, default=dict)),
                ('metadata', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')], max_length=20)),
                ('result', models.JSONField(default=dict)),
                ('notification_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='notification.notification')),
            ],
        ),
    ]
