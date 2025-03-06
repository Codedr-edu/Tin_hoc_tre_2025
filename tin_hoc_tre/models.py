from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator

'''
class Rank(models.Model):
    name = models.TextField()
    min_avg_point = models.FloatField()
    max_avg_point = models.FloatField()
'''


class Bio(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Bio_user")
    avatar = models.ImageField(upload_to="avatar/", null=True)
    thumbnail = models.ImageField(upload_to="thumbnail/", null=True)
    speaking_score = models.FloatField()
    writing_score = models.FloatField()
    listening_score = models.FloatField()
    reading_score = models.FloatField()
    grammar_score = models.FloatField()
    avg_score = models.FloatField()
    title = models.TextField()


class Level(models.Model):
    name = models.TextField()
    point = models.FloatField()
    gift_point = models.FloatField()


class Emoji(models.Model):
    name = models.TextField()
    color = models.TextField()


class Speaking_scripts(models.Model):
    title = models.TextField()
    description = models.TextField()
    speaker_script = models.FileField(
        upload_to="speaking/speaker/scripts/", null=True)
    speaker_script_AI = models.TextField(null=True)
    theme = models.TextField()
    image = models.ImageField(upload_to="speaking/image/", null=True)
    status = models.TextField()
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="level_speaking_scripts_result")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="speaking_scripts_user")


class Speaking_scripts_emoji(models.Model):
    speaking_scripts = models.ForeignKey(
        Speaking_scripts, on_delete=models.CASCADE, related_name="scripts_speaking_scripts_emoji")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_speaking_scripts_emoji")
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_speaking_scripts_emoji")


class Speaking_scripts_result(models.Model):
    speaking_scripts = models.ForeignKey(
        Speaking_scripts, on_delete=models.CASCADE, related_name="scripts_speaking_scripts_result")
    transcript_file = models.FileField(
        upload_to="speaking/user/transcript/", null=True)
    audio_file = models.FileField(upload_to="speaking/user/audio/", null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_speaking_scripts_result")
    review = models.TextField(null=True)
    status = models.TextField()


class Speaking_scripts_comment(models.Model):
    speaking_scripts = models.ForeignKey(
        Speaking_scripts, on_delete=models.CASCADE, related_name="comment_Speaking_scripts")
    content = models.TextField()
    like = models.ManyToManyField(
        Bio, related_name="like_comment_Speaking_scripts")
    dislike = models.ManyToManyField(
        Bio, related_name="dislike_comment_Speaking_scripts")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_comment_Speaking_scripts")
    status = models.TextField()


class Writting(models.Model):
    title = models.TextField()
    description = models.TextField()
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="writting_level")
    image = models.ImageField(upload_to="writting/image/")
    status = models.TextField()
    theme = models.TextField()
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="writing_user")
    # document = models.FileField(upload_to="writting/document/")
    # document_AI = models.TextField(null=True)


class Writting_emoji(models.Model):
    writting = models.ForeignKey(
        Writting, on_delete=models.CASCADE, related_name="scripts_writting_emoji")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_writting_emoji")
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_writting_emoji")


class Writting_result(models.Model):
    writting = models.ForeignKey(
        Writting, on_delete=models.CASCADE, related_name="scripts_writting_result")
    writting_content = models.TextField(null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_writting_result")
    review = models.TextField(null=True)
    status = models.TextField(null=True)


class Writting_comment(models.Model):
    writting = models.ForeignKey(
        Writting, on_delete=models.CASCADE, related_name="comment_writting")
    content = models.TextField()
    like = models.ManyToManyField(Bio, related_name="like_comment_writting")
    dislike = models.ManyToManyField(
        Bio, related_name="dislike_comment_writting")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_comment_writting")
    status = models.TextField()


class Reading(models.Model):
    title = models.TextField()
    description = models.TextField()
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="Reading_level")
    image = models.ImageField(upload_to="Reading/image/")
    # document = models.FileField(upload_to="Reading/document/")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="reading_user")
    status = models.TextField(null=True)


class Reading_question(models.Model):
    question = models.TextField()
    no_question = models.IntegerField()
    reading = models.ForeignKey(
        Reading, on_delete=models.CASCADE, related_name="reading_reading_question")


class Reading_emoji(models.Model):
    reading = models.ForeignKey(
        Reading, on_delete=models.CASCADE, related_name="scripts_reading_emoji")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_reading_emoji")
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_reading_emoji")


class Reading_result(models.Model):
    reading_question = models.ForeignKey(
        Reading_question, on_delete=models.CASCADE, related_name="scripts_reading_result")
    # Reading_file = models.FileField(upload_to="Reading/user/")
    answer = models.TextField()
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_reading_result")
    status = models.TextField()


class Reading_comment(models.Model):
    reading = models.ForeignKey(
        Reading, on_delete=models.CASCADE, related_name="comment_Reading")
    content = models.TextField()
    like = models.ManyToManyField(Bio, related_name="like_comment_Reading")
    dislike = models.ManyToManyField(
        Bio, related_name="dislike_comment_Reading")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_comment_Reading")
    status = models.TextField()


class Listening(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="Listening_level")
    image = models.ImageField(upload_to="Listening/image/")
    audio = models.FileField(upload_to="listening/file/", null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="listening_user")
    status = models.TextField(null=True)


class Listening_question(models.Model):
    question = models.TextField()
    no_question = models.IntegerField()
    listening = models.ForeignKey(
        Listening, on_delete=models.CASCADE, related_name="listening_listening_question")


class Listening_emoji(models.Model):
    listening = models.ForeignKey(
        Listening, on_delete=models.CASCADE, related_name="scripts_listening_emoji")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_listening_emoji")
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_listening_emoji")


class Listening_result(models.Model):
    listening_question = models.ForeignKey(
        Listening_question, on_delete=models.CASCADE, related_name="scripts_listening_result")
    # Reading_file = models.FileField(upload_to="Reading/user/")
    answer = models.TextField()
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_listening_result")
    status = models.TextField()


class Listening_comment(models.Model):
    listening = models.ForeignKey(
        Listening, on_delete=models.CASCADE, related_name="comment_Listening")
    content = models.TextField()
    like = models.ManyToManyField(Bio, related_name="like_comment_Listening")
    dislike = models.ManyToManyField(
        Bio, related_name="dislike_comment_Listening")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_comment_Listening")
    status = models.TextField()


"""
class Grammar(models.Model):
    title = models.TextField()
    description = models.TextField()
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="Grammar_level")
    image = models.ImageField(upload_to="Grammar/image/")
    document = models.FileField(upload_to="Grammar/document/")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="grammar_user")


class Grammar_emoji(models.Model):
    grammar = models.ForeignKey(
        Grammar, on_delete=models.CASCADE, related_name="scripts_speaking_scripts_emoji")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_speaking_scripts_emoji")
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_speaking_scripts_emoji")


class Grammar_result(models.Model):
    grammar = models.ForeignKey(
        Grammar, on_delete=models.CASCADE, related_name="scripts_speaking_scripts_result")
    grammar_file = models.FileField(upload_to="Grammar/user/")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_speaking_scripts_result")
    status = models.TextField()


class Grammar_comment(models.Model):
    grammar = models.ForeignKey(
        Grammar, on_delete=models.CASCADE, related_name="comment_Grammar")
    content = models.TextField()
    like = models.ManyToManyField(Bio, related_name="like_comment_Grammar")
    dislike = models.ManyToManyField(
        Bio, related_name="dislike_comment_Grammar")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_comment_Grammar")
    status = models.TextField()
"""


class Document(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True)
    grade = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="Document_auth", null=True)
    skill = models.TextField(null=True)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="document_level", null=True)
    file = models.FileField(upload_to="files/documents/", null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=1000, null=True)
    comment_counter = models.IntegerField(null=True)


class Document_emoji(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="scripts_document_emoji", null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_document_emoji", null=True)
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_document_emoji", null=True)


class have_buy_document(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="document_check", null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="Document_buyer", null=True)
    star = models.FloatField(null=True)


class Comment_Document(models.Model):
    content = models.TextField(null=True)
    user = models.ForeignKey(
        Bio, related_name='comment_document_user', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(
        Document, related_name='cmt_document', on_delete=models.CASCADE, null=True)


class Post(models.Model):
    content = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="post_auth_related")
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="post_down")
    datetime = models.DateTimeField(auto_now_add=True)
    comment_counter = models.IntegerField()


class Post_emoji(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="scripts_post_emoji", null=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_post_emoji", null=True)
    emoji = models.ForeignKey(
        Emoji, on_delete=models.CASCADE, related_name="emoji_post_emoji", null=True)


class Comment_Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Bio, related_name='comment_post_user_related', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Post, related_name='comment_post_related', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="comment_post_down")
