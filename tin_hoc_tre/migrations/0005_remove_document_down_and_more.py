# Generated by Django 5.1.5 on 2025-02-24 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tin_hoc_tre', '0004_document_comment_document_document_emoji_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='down',
        ),
        migrations.RemoveField(
            model_name='writting_result',
            name='writting_file',
        ),
        migrations.AddField(
            model_name='writting_result',
            name='writting_content',
            field=models.TextField(null=True),
        ),
    ]
