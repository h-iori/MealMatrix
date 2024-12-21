# Generated by Django 5.1.2 on 2024-12-17 08:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('age', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('diet_goal', models.CharField(max_length=50)),
                ('diet_time_period', models.CharField(max_length=20)),
                ('diet_plan_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
