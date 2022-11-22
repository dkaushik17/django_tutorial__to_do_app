# Generated by Django 4.0.2 on 2022-09-18 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todos', '0004_Task_model__added_created_and_modified_datetime_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
