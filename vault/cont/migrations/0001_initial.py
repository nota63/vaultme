# Generated by Django 5.0.6 on 2024-07-23 07:27

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
            name='Cont',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('relation', models.CharField(choices=[('mother', 'mother'), ('father', 'father'), ('family', 'family'), ('gf/bf', 'gf/bf'), ('others', 'others')], max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('important', 'important'), ('less', 'less')], max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
