# Generated by Django 5.0.6 on 2024-07-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devs', '0003_alter_collaborate_applying_for_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='files',
            field=models.FileField(upload_to='projects/'),
        ),
    ]
