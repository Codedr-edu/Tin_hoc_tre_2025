# Generated by Django 5.1.5 on 2025-02-12 04:00

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
            name='Emoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('color', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('point', models.FloatField()),
                ('gift_point', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='avatar/')),
                ('thumbnail', models.ImageField(upload_to='thumbnail/')),
                ('speaking_score', models.FloatField()),
                ('writing_score', models.FloatField()),
                ('listening_score', models.FloatField()),
                ('reading_score', models.FloatField()),
                ('grammar_score', models.FloatField()),
                ('avg_score', models.FloatField()),
                ('title', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bio_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(upload_to='Listening/image/')),
                ('audio', models.TextField(null=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Listening_level', to='tin_hoc_tre.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_user', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Listening_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.TextField()),
                ('dislike', models.ManyToManyField(related_name='dislike_comment_Listening', to='tin_hoc_tre.bio')),
                ('like', models.ManyToManyField(related_name='like_comment_Listening', to='tin_hoc_tre.bio')),
                ('listening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_Listening', to='tin_hoc_tre.listening')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment_Listening', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Listening_emoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emoji_listening_emoji', to='tin_hoc_tre.emoji')),
                ('listening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_listening_emoji', to='tin_hoc_tre.listening')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_listening_emoji', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Listening_question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('no_question', models.IntegerField()),
                ('listening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_listening_question', to='tin_hoc_tre.listening')),
            ],
        ),
        migrations.CreateModel(
            name='Listening_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('status', models.TextField()),
                ('listening_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_listening_result', to='tin_hoc_tre.listening_question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_listening_result', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='Reading/image/')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reading_level', to='tin_hoc_tre.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_user', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Reading_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.TextField()),
                ('dislike', models.ManyToManyField(related_name='dislike_comment_Reading', to='tin_hoc_tre.bio')),
                ('like', models.ManyToManyField(related_name='like_comment_Reading', to='tin_hoc_tre.bio')),
                ('reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_Reading', to='tin_hoc_tre.reading')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment_Reading', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Reading_emoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emoji_reading_emoji', to='tin_hoc_tre.emoji')),
                ('reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_reading_emoji', to='tin_hoc_tre.reading')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reading_emoji', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Reading_question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('no_question', models.IntegerField()),
                ('reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_reading_question', to='tin_hoc_tre.reading')),
            ],
        ),
        migrations.CreateModel(
            name='Reading_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('status', models.TextField()),
                ('reading_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_reading_result', to='tin_hoc_tre.reading_question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reading_result', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Speaking_scripts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('speaker_script', models.FileField(null=True, upload_to='speaking/speaker/scripts/')),
                ('speaker_script_AI', models.TextField(null=True)),
                ('theme', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='speaking/image/')),
                ('status', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level_speaking_scripts_result', to='tin_hoc_tre.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speaking_scripts_user', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Speaking_scripts_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.TextField()),
                ('dislike', models.ManyToManyField(related_name='dislike_comment_Speaking_scripts', to='tin_hoc_tre.bio')),
                ('like', models.ManyToManyField(related_name='like_comment_Speaking_scripts', to='tin_hoc_tre.bio')),
                ('speaking_scripts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_Speaking_scripts', to='tin_hoc_tre.speaking_scripts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment_Speaking_scripts', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Speaking_scripts_emoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emoji_speaking_scripts_emoji', to='tin_hoc_tre.emoji')),
                ('speaking_scripts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_speaking_scripts_emoji', to='tin_hoc_tre.speaking_scripts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_speaking_scripts_emoji', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Speaking_scripts_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript_file', models.FileField(null=True, upload_to='speaking/user/transcript/')),
                ('audio_file', models.FileField(null=True, upload_to='speaking/user/audio/')),
                ('review', models.TextField(null=True)),
                ('status', models.TextField()),
                ('speaking_scripts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_speaking_scripts_result', to='tin_hoc_tre.speaking_scripts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_speaking_scripts_result', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Writting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='writting/image/')),
                ('status', models.TextField()),
                ('theme', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writting_level', to='tin_hoc_tre.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writing_user', to='tin_hoc_tre.bio')),
            ],
        ),
        migrations.CreateModel(
            name='Writting_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.TextField()),
                ('dislike', models.ManyToManyField(related_name='dislike_comment_writting', to='tin_hoc_tre.bio')),
                ('like', models.ManyToManyField(related_name='like_comment_writting', to='tin_hoc_tre.bio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment_writting', to='tin_hoc_tre.bio')),
                ('writting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_writting', to='tin_hoc_tre.writting')),
            ],
        ),
        migrations.CreateModel(
            name='Writting_emoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emoji_writting_emoji', to='tin_hoc_tre.emoji')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_writting_emoji', to='tin_hoc_tre.bio')),
                ('writting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_writting_emoji', to='tin_hoc_tre.writting')),
            ],
        ),
        migrations.CreateModel(
            name='Writting_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writting_file', models.FileField(upload_to='writting/user/')),
                ('review', models.TextField(null=True)),
                ('status', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_writting_result', to='tin_hoc_tre.bio')),
                ('writting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts_writting_result', to='tin_hoc_tre.writting')),
            ],
        ),
    ]
