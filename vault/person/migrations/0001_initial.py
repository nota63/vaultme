# Generated by Django 5.0.6 on 2024-07-23 14:33

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
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('connection', models.CharField(choices=[('brother', 'brother'), ('family member', 'family member'), ('stranger', 'stranger'), ('special', 'special'), ('freind', 'freind'), ('other', 'other')], max_length=100)),
                ('social_id', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('instagram', 'instagram'), ('facebook', 'facebook'), ('twitter', 'twitter'), ('other', 'other')], max_length=100)),
                ('special_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
