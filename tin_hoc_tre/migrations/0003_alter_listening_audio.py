# Generated by Django 5.1.5 on 2025-02-14 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tin_hoc_tre', '0002_listening_status_reading_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listening',
            name='audio',
            field=models.FileField(null=True, upload_to='listening/file/'),
        ),
    ]
