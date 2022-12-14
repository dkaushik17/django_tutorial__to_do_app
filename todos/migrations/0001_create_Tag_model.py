# Generated by Django 4.0.2 on 2022-09-17 05:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'db_table': 'tags',
            },
        ),
    ]
