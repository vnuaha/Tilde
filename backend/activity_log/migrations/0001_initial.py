# Generated by Django 3.1.4 on 2021-12-23 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_1_id', models.PositiveIntegerField(blank=True, null=True)),
                ('object_2_id', models.PositiveIntegerField(blank=True, null=True)),
                ('actor_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='log_entries_as_actor', to=settings.AUTH_USER_MODEL)),
                ('effected_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='log_entries_as_effected_user', to=settings.AUTH_USER_MODEL)),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='activity_log.eventtype')),
                ('object_1_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_entries_object_1_set', to='contenttypes.contenttype')),
                ('object_2_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_entries_object_2_set', to='contenttypes.contenttype')),
            ],
        ),
    ]
