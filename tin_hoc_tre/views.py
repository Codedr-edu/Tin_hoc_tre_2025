from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.apps import AppConfig
import random
from django.db.models import Q
from django.core.files.base import ContentFile
import datetime
import json
import hashlib
import os
from .speakingGPT import *
from .writtingGPT import *
from .readingGPT import *
from .listeningGPT import *
from .listeningAudioMaker import *
import io
from .GPTsecurity import check_document, check_image, check_content
from .improveGPT import *
from .utils import *


def index(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        return redirect("my_speaking_scripts_workspace")
    else:
        bio = None
    context = {"bio": bio}
    return render(request, "index.html", context=context)


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("check")
        else:
            return redirect("index")


def Signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        avatar = request.FILES['avatar']
        thumbnail = request.FILES['thumbnail']

        user = User.objects.filter(username=username).first()
        user2 = Bio.objects.filter(user=user).first()

        if not user and not user2:
            user = User.objects.create_user(username, email, password)
            user.save()
            bio = Bio(user=user, avatar=avatar, thumbnail=thumbnail, speaking_score=0,
                      writing_score=0, reading_score=0, grammar_score=0, listening_score=0, avg_score=0)
            bio.save()
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect("check")
        else:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("check")


def check(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if bio:
            return redirect('my_speaking_scripts_workspace')
        else:
            if request.method == "POST":
                avatar = request.FILES['avatar']
                thumbnail = request.FILES['thumbnail']
                passcode = request.POST.get("passcode")

                bio = Bio(user=request.user, avatar=avatar, thumbnail=thumbnail, speaking_score=0,
                          writing_score=0, reading_score=0, grammar_score=0, listening_score=0, avg_score=0)
                bio.save()
                return redirect('my_speaking_scripts_workspace')
    else:
        return redirect('index')
    return render(request, 'check.html')


def create_speaking_scripts_AI(request):
    if request.user.is_authenticated:
        lv_list = Level.objects.all()
        bio = Bio.objects.filter(user=request.user).first()
        context = {"levels": lv_list}
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            level = request.POST.get("level")
            # image = request.FILES.get("image")
            theme = request.POST.get("theme")

            level = Level.objects.filter(id=level).first()
            sql = Speaking_scripts(title=title, description=description, user=bio,
                                   level=level, status="Không công khai")
            sql.save()

            scripts = speaking_scripts_maker(level=level.name, theme=theme)
            a = scripts.split("\n")
            b = str(sql.id)+".txt"
            content = ""
            # scripts_file = open(b, "w")
            for i in a:
                if len(i) > 0:
                    content += i+"\n"
            # scripts_file.close()
            # Generate the text file content
            file_content = content

            # Create a TextFile instance

            # Save the content to a file
            file_name = str(sql.id)+'.txt'
            sql.speaker_script.save(file_name, ContentFile(file_content))

            # Save the TextFile instance to the database
            sql.save()
            return redirect("my_speaking_scripts_workspace")
    else:
        return redirect("check")
    return render(request, "speaking/AI/create.html", context=context)


def create_writting_AI(request):
    if request.user.is_authenticated:
        lv_list = Level.objects.all()
        bio = Bio.objects.filter(user=request.user).first()
        context = {"levels": lv_list}
        if request.method == "POST":
            level = request.POST.get("level")
            # image = request.FILES.get("image")
            theme = request.POST.get("theme")

            level = Level.objects.filter(id=level).first()
            title = writting_topic_maker(level=level.name, theme=theme)
            description = writting_require_maker(level=level.name, title=title)
            sql = Writting(title=title, description=description,
                           user=bio, level=level, status="Không công khai")
            sql.save()

            return redirect("my_writting_workspace")
    else:
        return redirect("check")
    return render(request, "writting/AI/create.html", context=context)


def create_reading_AI(request):
    if request.user.is_authenticated:
        lv_list = Level.objects.all()
        bio = Bio.objects.filter(user=request.user).first()
        context = {"levels": lv_list}
        if request.method == "POST":
            level = request.POST.get("level")
            # image = request.FILES.get("image")
            theme = request.POST.get("theme")

            level = Level.objects.filter(id=level).first()
            description1 = reading_maker(level=level.name, theme=theme)
            title = reading_title_maker(level=level.name, essay=description1)
            description = description1.replace("\n", "<br>")
            sql = Reading(title=title, description=description, user=bio,
                          level=level, status="Không công khai")
            sql.save()
            questions = reading_question_maker(
                essay=description1, level=level.name)
            a = questions.split("\n")
            for i in a:
                if len(i) > 0:
                    sql2 = Reading_question.objects.filter(reading=sql).count()
                    sql1 = Reading_question(
                        question=i, reading=sql, no_question=sql2+1)
                    sql1.save()

            # questions =
            return redirect("my_reading_workspace")
    else:
        return redirect("check")
    return render(request, "reading/AI/create.html", context=context)


def create_listening_AI(request):
    if request.user.is_authenticated:
        lv_list = Level.objects.all()
        context = {"levels": lv_list}
        bio = Bio.objects.filter(user=request.user).first()
        if request.method == "POST":
            title = request.POST.get("title")
            # description = request.POST.get("description")
            level = request.POST.get("level")
            # image = request.FILES.get("image")
            theme = request.POST.get("theme")

            level = Level.objects.filter(id=level).first()
            sql = Listening(title=title, level=level,
                            status="Không công khai", user=bio)
            sql.save()

            scripts = listening_scripts_maker(level=level.name, theme=theme)
            sql.description = scripts.replace("\n", "<br>")
            sql.save()
            # a = scripts.split("?\n")
           # b = "AI_file/listening/scripts/"+str(sql.id)+".mp3"
            audio_file = text_to_speech_file(text=scripts, id=sql.id)

            response = HttpResponse(content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{sql.id}.mp3"'

            # Convert HttpResponse content to a file-like object
            for chunk in audio_file:
                if chunk:
                    response.write(chunk)
            file_content = io.BytesIO(response.content)

            # Create a new instance of MyModel

            # Save the file content to the FileField
            sql.audio.save(f'{sql.id}.mp3', ContentFile(
                file_content.getvalue()))

            # Save the instance to the database
            sql.save()

            questions = listening_question_maker(
                essay=scripts, level=level.name)
            a = questions.split("\n")
            for i in a:
                if len(i) > 0:
                    sql2 = Listening_question.objects.filter(
                        listening=sql).count()
                    sql1 = Listening_question(
                        question=i, listening=sql, no_question=sql2+1)
                    sql1.save()

            return redirect("my_listening_workspace")
    else:
        return redirect("check")
    return render(request, "listening/AI/create.html", context=context)


def my_listening_workspace(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Listening.objects.filter(user=bio).all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Listening.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, user=bio).all()
            elif search and not sub:
                post = Listening.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), user=bio).all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Listening.objects.filter(
                    level=sub, user=bio).all()
        else:
            post = Listening.objects.filter(user=bio).all()
        context = {"bio": bio, "posts": post[::-1], 'subjects': level}
    else:
        return redirect("check")
    return render(request, "listening/workspace.html", context=context)


def my_reading_workspace(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Reading.objects.filter(user=bio).all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Reading.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, user=bio).all()
            elif search and not sub:
                post = Reading.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), user=bio).all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Reading.objects.filter(
                    level=sub, user=bio).all()
        else:
            post = Reading.objects.filter(user=bio).all()
        context = {"bio": bio, "posts": post[::-1], 'subjects': level}
    else:
        return redirect("check")
    return render(request, "reading/workspace.html", context=context)


def my_writting_workspace(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Writting.objects.filter(user=bio).all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Writting.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, user=bio).all()
            elif search and not sub:
                post = Writting.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), user=bio).all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Writting.objects.filter(
                    level=sub, user=bio).all()
        else:
            post = Writting.objects.filter(user=bio).all()
        context = {"bio": bio, "posts": post[::-1], 'subjects': level}
    else:
        return redirect("check")
    return render(request, "writting/workspace.html", context=context)


def my_speaking_scripts_workspace(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Speaking_scripts.objects.filter(user=bio).all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Speaking_scripts.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, user=bio).all()
            elif search and not sub:
                post = Speaking_scripts.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), user=bio).all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Speaking_scripts.objects.filter(
                    level=sub, user=bio).all()
        else:
            post = Speaking_scripts.objects.filter(user=bio).all()
        context = {"bio": bio, "posts": post[::-1], 'subjects': level}
    else:
        return redirect("check")
    return render(request, "speaking/workspace.html", context=context)


def speaking_scripts_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts.objects.filter(id=id).first()
        emoji = Emoji.objects.all()
        interact = Speaking_scripts_emoji.objects.filter(
            speaking_scripts=post).count()
        my_emoji = Speaking_scripts_emoji.objects.filter(
            speaking_scripts=post, user=bio).first()
        comment = Speaking_scripts_comment.objects.filter(
            speaking_scripts=post).all()
        result = Speaking_scripts_result.objects.filter(
            speaking_scripts=post).all().count()
        if post.status == "Không công khai" and post.user != bio:
            return redirect("my_speaking_scripts_workspace")
        elif post.user == bio:
            check = True
        else:
            check = False
        my_result = Speaking_scripts_result.objects.filter(
            speaking_scripts=post, user=bio).last()
        context = {"bio": bio, "post": post, "comments": comment, "my_emoji": my_emoji, "interact": interact,
                   "emojies": emoji, "result": result, "my_result": my_result, "check": check}
    else:
        return redirect("check")
    return render(request, "speaking/view.html", context=context)


def listening_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening.objects.filter(id=id).first()
        emoji = Emoji.objects.all()
        interact = Listening_emoji.objects.filter(
            listening=post).count()
        my_emoji = Listening_emoji.objects.filter(user=bio).last()
        comment = Listening_comment.objects.filter(listenings=post).all()
        result = Listening_result.objects.all(listenings=post).count()
        my_result = Listening_result.objects.filter(
            listenings=post, user=bio).last()
        results = Listening_result.objects.filter(listenings=post).all()
        if post.status == "Không công khai" and post.user != bio:
            return redirect("my_listenings_workspace")
        elif post.user == bio:
            check = True
        else:
            check = False
        context = {"bio": bio, "post": post, "comments": comment, "my_emoji": my_emoji, "interact": interact,
                   "emojies": emoji, "result": result, "my_result": my_result, "check": check, "results": results}
    else:
        return redirect("check")
    return render(request, "listening/view.html", context=context)


def writting_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting.objects.filter(id=id).first()
        emoji = Emoji.objects.all()
        interact = Writting_emoji.objects.filter(
            writting=post).count()
        my_emoji = Writting_emoji.objects.filter(
            writting=post, user=bio).last()
        comment = Writting_comment.objects.filter(writting=post).all()
        result = Writting_result.objects.filter(writting=post).all().count()
        my_result = Writting_result.objects.filter(
            writting=post, user=bio).last()
        if post.status == "Không công khai" and post.user != bio:
            return redirect("my_writting_workspace")
        elif post.user == bio:
            check = True
        else:
            check = False
        context = {"bio": bio, "post": post, "comments": comment, "my_emoji": my_emoji, "interact": interact,
                   "emojies": emoji, "result": result, "my_result": my_result, "check": check}
    else:
        return redirect("check")
    return render(request, "writting/view.html", context=context)


def reading_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading.objects.filter(id=id).first()
        emoji = Emoji.objects.all()
        interact = Reading_emoji.objects.filter(
            reading=post).count()
        my_emoji = Reading_emoji.objects.filter(reading=post, user=bio).last()
        comment = Reading_comment.objects.filter(reading=post).all()
        result = Reading_result.objects.filter(
            reading_question__reading=post).all().count()
        my_result = Reading_result.objects.filter(
            reading_question__reading=post, user=bio).last()
        results = Reading_result.objects.filter(
            reading_question__reading=post, user=bio).all()
        if post.status == "Không công khai" and post.user != bio:
            return redirect("my_reading_workspace")
        elif post.user == bio:
            check = True
        else:
            check = False
        context = {"bio": bio, "post": post, "comments": comment, "my_emoji": my_emoji, "interact": interact,
                   "emojies": emoji, "result": result, "my_result": my_result, "check": check, "results": results}
    else:
        return redirect("check")
    return render(request, "reading/view.html", context=context)


def reading_emoji(request, id, emoji_id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading_emoji.objects.filter(user=bio, reading__id=id).first()
        emoji = Emoji.objects.filter(id=emoji_id).first()
        if post:
            if post.emoji == emoji:
                post.delete()
            return redirect("reading_view", id=id)
        else:
            post = Reading.objects.filter(id=id).first()
            sql = Reading_emoji(
                reading=post, emoji=emoji, user=bio)
            sql.save()
            return redirect("reading_view", id=id)


def writting_emoji(request, id, emoji_id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting_emoji.objects.filter(user=bio, writting__id=id).first()
        emoji = Emoji.objects.filter(id=emoji_id).first()
        if post:
            if post.emoji == emoji:
                post.delete()
            return redirect("writting_view", id=id)
        else:
            post = Writting.objects.filter(id=id).first()
            sql = Writting_emoji(
                writting=post, emoji=emoji, user=bio)
            sql.save()
            return redirect("writting_view", id=id)


def listening_emoji(request, id, emoji_id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening_emoji.objects.filter(
            user=bio, listening__id=id).first()
        emoji = Emoji.objects.filter(id=emoji_id).first()
        if post:
            if post.emoji == emoji:
                post.delete()
            return redirect("listening_view", id=id)
        else:
            post = Listening.objects.filter(id=id).first()
            sql = Listening_emoji(
                listening=post, emoji=emoji, user=bio)
            sql.save()
            return redirect("listening_view", id=id)


def speaking_scripts_emoji(request, id, emoji_id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts_emoji.objects.filter(
            user=bio, speaking_scripts__id=id).first()
        emoji = Emoji.objects.filter(id=emoji_id).first()
        if post:
            if post.emoji == emoji:
                post.delete()
            return redirect("speaking_scripts_view", id=id)
        else:
            post = Speaking_scripts.objects.filter(id=id).first()
            sql = Speaking_scripts_emoji(
                speaking_scripts=post, emoji=emoji, user=bio)
            sql.save()
            return redirect("speaking_scripts_view", id=id)


def speaking_scripts_comment(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Speaking_scripts_comment(
                speaking_scripts=post, user=bio, content=content)
            sql.save()
            return redirect("speaking_scripts_view", id=id)
    else:
        return redirect("check")


def reading_comment(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Reading_comment(reading=post, user=bio, content=content)
            sql.save()
            return redirect("reading_view", id=id)
    else:
        return redirect("check")


def writting_comment(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Writting_comment(writting=post, user=bio, content=content)
            sql.save()
            return redirect("writting_view", id=id)
    else:
        return redirect("check")


def listening_comment(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Listening_comment(listening=post, user=bio, content=content)
            sql.save()
            return redirect("listening_view", id=id)
    else:
        return redirect("check")


def writting_submit(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Writting_result(
                writting=post, writting_content=content.replace("\n", "<br>"), user=bio)
            sql.save()

            grader = writting_grader(
                essay=sql.writting_content, title=post.title, level=post.level.name)
            reviewer = writting_reviewer(
                essay=sql.writting_content, title=post.title, level=post.level.name)

            if grader == "Đạt":
                sql.status = "Đạt"
                sql.save()
                bio.writing_score += post.level.point
                bio.save()
            else:
                sql.status = "Không Đạt"
                sql.save()

            review = reviewer.replace("\n", "<br>")
            sql.review = review
            sql.save()

            return redirect("writting_result_view", id=sql.id)
        context = {"bio": bio, "post": post}
    else:
        return redirect("check")
    return render(request, "writting/submit.html", context=context)


def speaking_submit(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts.objects.filter(id=id).first()
        if request.method == "POST":
            transcript_file = request.FILES.get("transcript_file")
            audio_file = request.FILES.get("audio_file")

            sql = Speaking_scripts_result(
                speaking_scripts=post, transcript_file=transcript_file, audio_file=audio_file, user=bio)
            sql.save()

            file_path = sql.transcript_file.path
            with open(file_path, 'r') as file:
                content = file.read()

            question_file = open(post.speaker_script.path, 'r')
            question_file.read()

            grader = speaking_grader(
                essay=content, title=question_file, level=post.level.name)
            reviewer = speaking_reviewer(
                essay=content, title=question_file, level=post.level.name)

            if grader == "Đạt":
                sql.status = "Đạt"
                sql.save()
                bio.reading_score += post.level.point
                bio.save()
            else:
                sql.status = "Không Đạt"
                sql.save()

            review = reviewer.replace("\n", "<br>")
            sql.review = review
            sql.save()

            return redirect("speaking_scripts_result_view", id=sql.id)
        context = {"bio": bio, "post": post}
    else:
        return redirect("check")
    return render(request, "speaking/submit.html", context=context)


def reading_submit(request, id, number):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading.objects.filter(id=id).first()
        question = Reading_question.objects.filter(
            reading=post, no_question=number).first()
        r = range(1, 6)
        next_question = number+1
        if request.method == "POST":
            answer = request.POST.get("answer")
            grader = reading_question_grader(
                question=question.question, essay=post.description, level=post.level.name, answer=answer)

            sql = Reading_result(reading_question=question,
                                 answer=answer, user=bio)
            sql.save()

            if grader == "Đạt":
                sql.status = "Đạt"
                sql.save()
                bio.reading_score += post.level.point / 5
                bio.save()
            else:
                sql.status = "Không Đạt"
                sql.save()

            return redirect("reading_result_view", id=sql.id)
        context = {"bio": bio, "post": post, "question": question,
                   "r": r, "next_question": next_question}
    else:
        return redirect("check")
    return render(request, "reading/submit.html", context=context)


def listening_submit(request, id, number):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening.objects.filter(id=id).first()
        question = Listening_question.objects.filter(
            listening=post, no_question=number).first()
        r = range(1, 6)
        next_question = number+1
        if request.method == "POST":
            answer = request.POST.get("answer")
            grader = listening_question_grader(
                question=question.question, essay=post.description, level=post.level.name, answer=answer)

            sql = Listening_result(
                listening_question=question, answer=answer, user=bio)
            sql.save()

            if grader == "Đạt":
                sql.status = "Đạt"
                sql.save()
                bio.reading_score += post.level.point / 5
                bio.save()
            else:
                sql.status = "Không Đạt"
                sql.save()

            return redirect("listening_result_view", id=sql.id)
        context = {"bio": bio, "post": post, "question": question,
                   "r": r, "next_question": next_question}
    else:
        return redirect("check")
    return render(request, "listening/submit.html", context=context)


def change_status_writting(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting.objects.filter(id=id, user=bio).first()
        if post:
            if request.method == "POST":
                status = request.POST.get("status")
                description = request.POST.get("description")

                if description:
                    post.review = description.replace("\n", "<br>")
                post.status = status
                post.save()
                return redirect("writting_view", id=id)
        else:
            return redirect("my_writting_workspace")
    else:
        return redirect("check")


def change_status_listening(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening.objects.filter(id=id, user=bio).first()
        if post:
            if request.method == "POST":
                status = request.POST.get("status")
                description = request.POST.get("description")

                if description:
                    post.review = description.replace("\n", "<br>")
                post.status = status
                post.save()
                return redirect("listening_view", id=id)
        else:
            return redirect("my_listening_workspace")
    else:
        return redirect("check")


def change_status_reading(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading.objects.filter(id=id, user=bio).first()
        if post:
            if request.method == "POST":
                status = request.POST.get("status")

                post.status = status
                post.save()
                return redirect("reading_view", id=id)
        else:
            return redirect("my_reading_workspace")
    else:
        return redirect("check")


def change_status_speaking_scripts(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts.objects.filter(id=id, user=bio).first()
        if post:
            if request.method == "POST":
                status = request.POST.get("status")

                post.status = status
                post.save()
                return redirect("speaking_scripts_view", id=id)
        else:
            return redirect("my_speaking_scripts_workspace")
    else:
        return redirect("check")


def reading_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading_result.objects.filter(id=id).first()
        r = range(1, 6)
        next_question = post.reading_question.no_question+1
        context = {"bio": bio, "post": post,
                   'r': r, "next_question": next_question}
    else:
        return redirect("check")
    return render(request, "reading/result.html", context=context)


def listening_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening_result.objects.filter(id=id).first()
        r = range(1, 6)
        next_question = post.listening_question.no_question+1
        context = {"bio": bio, "post": post,
                   'r': r, "next_question": next_question}
    else:
        return redirect("check")
    return render(request, "listening/result.html", context=context)


def writting_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting_result.objects.filter(id=id).first()
        context = {"bio": bio, "post": post}
    else:
        return redirect("check")
    return render(request, "writting/result.html", context=context)


def speaking_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts_result.objects.filter(id=id).first()

        context = {"bio": bio, "post": post}
    else:
        return redirect("check")
    return render(request, "speaking/result.html", context=context)


def speaking_list_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts_result.objects.filter(
            speaking_scripts__id=id).all()
        a = Speaking_scripts.objects.filter(id=id).first()
        context = {"bio": bio,
                   "posts": post[::-1], "id": id, "a": a.level.name}
    else:
        return redirect("check")
    return render(request, "speaking/list_result.html", context=context)


def writting_list_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting_result.objects.filter(writting__id=id).all()
        a = Writting.objects.filter(id=id).first()
        context = {"bio": bio,
                   "posts": post[::-1], "id": id, "a": a.level.name}
    else:
        return redirect("check")
    return render(request, "writting/list_result.html", context=context)


def reading_list_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading_result.objects.filter(
            reading_question__reading__id=id).all()
        a = Reading.objects.filter(id=id).first()
        context = {"bio": bio,
                   "posts": post[::-1], "id": id, "a": a.level.name}
    else:
        return redirect("check")
    return render(request, "reading/list_result.html", context=context)


def listening_list_result_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening_result.objects.filter(
            listening_question__listening__id=id).all()
        a = Listening.objects.filter(id=id).first()
        context = {"bio": bio,
                   "posts": post[::-1], "id": id, "a": a.level.name}
    else:
        return redirect("check")
    return render(request, "listening/list_result.html", context=context)


def writting_status_change(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Writting_result.objects.filter(id=id).first()
        if request.method == "POST":
            status = request.POST.get("status")
            description = request.POST.get("description")

            post.status = status
            post.review = description
            post.save()
            return redirect("writting_list_result_view", id=post.writting.id)
    else:
        return redirect("check")


def reading_status_change(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading_result.objects.filter(id=id).first()
        if request.method == "POST":
            status = request.POST.get("status")
            # description = request.POST.get("description")

            post.status = status
            # post.review = description
            post.save()
            return redirect("reading_list_result_view", id=post.reading_question.reading.id)
    else:
        return redirect("check")


def listening_status_change(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening_result.objects.filter(id=id).first()
        if request.method == "POST":
            status = request.POST.get("status")
            # description = request.POST.get("description")

            post.status = status
            # post.review = description
            post.save()
            return redirect("listening_list_result_view", id=post.listening_question.listening.id)
    else:
        return redirect("check")


def speaking_status_change(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Speaking_scripts_result.objects.filter(id=id).first()
        if request.method == "POST":
            status = request.POST.get("status")
            description = request.POST.get("description")

            post.status = status
            post.review = description
            post.save()
            return redirect("speaking_list_result_view", id=post.speaking_scripts.id)
    else:
        return redirect("check")


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")
    else:
        return redirect("index")


def user_profile(request, id):
    if request.user.is_authenticated:
        your_bio = Bio.objects.filter(user=request.user).first()
        bio = Bio.objects.filter(id=id).first()
        if bio == your_bio:
            return redirect("my_profile")
        else:
            writting = Writting_result.objects.filter(user=bio).all()
            speaking = Speaking_scripts_result.objects.filter(user=bio).all()
            reading = Reading_result.objects.filter(user=bio).all()
            listening = Listening_result.objects.filter(user=bio).all()

            bio.writing_score = writting_point(writting)
            bio.speaking_score = speaking_point(speaking)
            bio.reading_score = reading_point(reading)
            bio.listening_score = listening_point(listening)
            bio.save()

            bio.avg_score = (bio.speaking_score + bio.listening_score +
                             bio.reading_score + bio.writing_score)/4
            bio.save()
            context = {'user': bio, 'writting': writting,
                       "speaking": speaking, "reading": reading, "listening": listening}
    else:
        return redirect("index")
    return render(request, "user/user_profile.html", context)


def my_profile(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        writting = Writting_result.objects.filter(user=bio).all()
        speaking = Speaking_scripts_result.objects.filter(user=bio).all()
        reading = Reading_result.objects.filter(user=bio).all()
        listening = Listening_result.objects.filter(user=bio).all()

        bio.writing_score = writting_point(writting)
        bio.speaking_score = speaking_point(speaking)
        bio.reading_score = reading_point(reading)
        bio.listening_score = listening_point(listening)
        bio.save()

        bio.avg_score = (bio.writing_score + bio.speaking_score +
                         bio.listening_score + bio.reading_score)/4
        bio.save()

        check = True
        context = {'user': bio, 'check': check, 'writting': writting,
                   "speaking": speaking, "reading": reading, "listening": listening}
    else:
        return redirect("index")
    return render(request, "user/user_profile.html", context)


def download_speaking_scripts_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Speaking_scripts.objects.filter(id=id).first()
        name = document.speaker_script.url.split("/")
        if bio and document:
            response = HttpResponse(document.speaker_script)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{name[-1]}"'
            return response
        # return redirect("question_view", id=document.question.id)


def download_listening_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Speaking_scripts.objects.filter(id=id).first()
        name = document.audio.url.split("/")
        if bio and document:
            response = HttpResponse(document.audio)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{name[-1]}"'
            return response
        # return redirect("question_view", id=document.question.id)


'''
def download_writting_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Writting_result.objects.filter(id=id).first()
        name = document.writting_file.url.split("/")
        if bio and document:
            response = HttpResponse(document.writting_file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{name[-1]}"'
            return response
        # return redirect("question_view", id=document.question.id)
'''


def download_transcript_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Speaking_scripts_result.objects.filter(id=id).first()
        name = document.transcript_file.url.split("/")
        if bio and document:
            response = HttpResponse(document.transcript_file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{name[-1]}"'
            return response


def download_audio_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Speaking_scripts_result.objects.filter(id=id).first()
        name = document.audio_file.url.split("/")
        if bio and document:
            response = HttpResponse(document.audio_file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{name[-1]}"'
            return response


def post_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        cmt = Comment_Post.objects
        emoji = Emoji.objects.all()
        if request.method == "GET":
            search = request.GET.get("search")
            if search:
                post = Post.objects.filter(
                    Q(content__icontains=search), status="Công khai").all()
            else:
                post = Post.objects.filter(status="Công khai").all()
        else:
            post = Post.objects.filter(status="Công khai").all()

        context = {"posts": post[::-1], "bio": bio,
                   "emojies": emoji, "cmts": cmt}
    else:
        return redirect("check")
    return render(request, "post/list.html", context)


def document_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        subject = Level.objects.all()

        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Document.objects.filter(status="Công khai").all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Document.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), subject=sub, status="Công khai").all()
            elif search and not sub:
                post = Document.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), status="Công khai").all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Document.objects.filter(
                    subject=sub, status="Công khai").all()
        else:
            post = Document.objects.filter(status="Công khai").all()

        context = {"posts": post[::-1], "bio": bio,
                   'subjects': subject}
    else:
        return redirect("index")
    return render(request, "document/list.html", context)


def post_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.filter(user=request.user).first()
        # bad = bad_keyword.objects.filter(status="Cấm").all()
        if request.method == "POST":
            content = request.POST.get("content")
            image = request.FILES.get("image")
            # video = request.FILE.get("video")

            sql = Post(content=content, user=user, image=image,
                       status="Chờ kiểm duyệt", comment_counter=0)
            sql.save()

            check_cnt = check_content(content)
            if sql.image:
                check_img = check_image(image=sql.image.url)
            else:
                check_img = "Pass"
            fail = "có nội dung nhạy cảm."
            fail3 = "Có nội dung nhạy cảm."
            fail2 = "I'm sorry，but I can't assist with that request"
            if (check_cnt == fail or check_cnt == fail2 or check_cnt == fail3) and (check_img == fail or check_img == fail2 or check_img == fail3):
                sql.status = "Chờ kiểm duyệt"
                sql.save()
            else:
                sql.status = "Công khai"
                sql.content = sql.content.replace("\n", "<br>")
                sql.save()

            return redirect("success", status=sql.status)
    else:
        return redirect("index")


def document_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            image = request.FILES.get("image")
            file = request.FILES.get('file')
            subject = request.POST.get("level")

            subject = Level.objects.get(id=subject)

            sql = Document(title=title, description=description, file=file,
                           image=image, status="Chờ kiểm duyệt", level=subject)
            sql.save()
            # sql = Document.objects.filter()

            check_doc = check_document(image=sql.file.url)
            if sql.image:
                check_img = check_image(image=sql.image.url)
            else:
                check_img = "Pass"
            check_title = check_content(sql.title)
            check_description = check_content(sql.description)
            fail = "có nội dung nhạy cảm."
            fail3 = "Có nội dung nhạy cảm."
            fail2 = "I'm sorry，but I can't assist with that request"
            if (check_doc == fail or check_doc == fail3 or check_doc == fail2) and (check_img == fail or check_img == fail3 or check_img == fail2) and (check_title == fail or check_title == fail2 or check_title == fail3) and (check_description == fail or check_description == fail2 or check_description == fail3):
                sql.status = "Chờ kiểm duyệt"
                sql.save()
            else:
                sql.status = "Công khai"
                sql.description = sql.description.replace("\n", "<br>")
                sql.save()

            return redirect("success", status=sql.status)
    else:
        return redirect("index")


def success(request, status):
    if request.user.is_authenticated:
        return render(request, "success.html", context={"status": status})
    else:
        return redirect("check")


def post_comment(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Comment_Post(post=post, user=bio, content=content)
            sql.save()
            return redirect("post_view", id=id)
    else:
        return redirect("check")


def document_comment(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Listening.objects.filter(id=id).first()
        if request.method == "POST":
            content = request.POST.get("content")

            sql = Comment_Document(document=post, user=bio, content=content)
            sql.save()
            return redirect("post_view", id=id)
    else:
        return redirect("check")


def listening_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        check2 = True
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Listening.objects.filter(status="Công khai").all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Listening.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, status="Công khai").all()
            elif search and not sub:
                post = Listening.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), status="Công khai").all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Listening.objects.filter(
                    level=sub, status="Công khai").all()
        else:
            post = Listening.objects.filter(user=bio, status="Công khai").all()
        context = {"bio": bio,
                   "posts": post[::-1], 'subjects': level, 'c2': check2}
    else:
        return redirect("check")
    return render(request, "listening/workspace.html", context=context)


def reading_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        check2 = True
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Reading.objects.filter(status="Công khai").all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Reading.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), status="Công khai", level=sub).all()
            elif search and not sub:
                post = Reading.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), status="Công khai").all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Reading.objects.filter(
                    level=sub, status="Công khai").all()
        else:
            post = Reading.objects.filter(user=bio).all()
        context = {"bio": bio,
                   "posts": post[::-1], 'subjects': level, 'c2': check2}
    else:
        return redirect("check")
    return render(request, "reading/workspace.html", context=context)


def writting_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        check2 = True
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Writting.objects.filter(status="Công khai").all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Writting.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, status="Công khai").all()
            elif search and not sub:
                post = Writting.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), status="Công khai").all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Writting.objects.filter(
                    level=sub, status="Công khai").all()
        else:
            post = Writting.objects.filter(user=bio).all()
        context = {"bio": bio,
                   "posts": post[::-1], 'subjects': level, 'c2': check2}
    else:
        return redirect("check")
    return render(request, "writting/workspace.html", context=context)


def speaking_scripts_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        level = Level.objects.all()
        check2 = True
        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Speaking_scripts.objects.filter(
                    status="Công khai").all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Speaking_scripts.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), level=sub, status="Công khai").all()
            elif search and not sub:
                post = Speaking_scripts.objects.filter(
                    Q(description__icontains=search), Q(title__icontains=search), status="Công khai").all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Speaking_scripts.objects.filter(
                    level=sub, status="Công khai").all()
        else:
            post = Speaking_scripts.objects.filter(user=bio).all()
        context = {"bio": bio,
                   "posts": post[::-1], 'subjects': level, 'c2': check2}
    else:
        return redirect("check")
    return render(request, "speaking/workspace.html", context=context)


def document_emoji(request, id, emoji_id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Reading_emoji.objects.filter(user=bio, reading__id=id).first()
        emoji = Emoji.objects.filter(id=emoji_id).first()
        if post:
            if post.emoji == emoji:
                post.delete()
            return redirect("reading_view", id=id)
        else:
            post = Reading.objects.filter(id=id).first()
            sql = Reading_emoji(
                reading=post, emoji=emoji, user=bio)
            sql.save()
            return redirect("reading_view", id=id)


def post_emoji(request, id, emoji_id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post_emoji.objects.filter(user=bio, post__id=id).first()
        emoji = Emoji.objects.filter(id=emoji_id).first()
        if post:
            if post.emoji == emoji:
                post.delete()
            return redirect("post_list_view")
        else:
            post = Post.objects.filter(id=id).first()
            sql = Post_emoji(
                post=post, emoji=emoji, user=bio)
            sql.save()
            return redirect("post_list_view")


def document_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Document.objects.filter(id=id, status="Công khai").first()
        check = have_buy_document.objects.filter(
            document=document, user=bio).first()
        noti = Comment_Document.objects.filter(
            post=document, status="Công khai").all()
        context = {'post': document, "comments": noti,
                   'check': check, "bio": bio}
    else:
        return redirect('check')
    return render(request, 'document/view.html', context)


def staff_document_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        subject = Level.objects.all()

        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Document.objects.filter().all()
            elif search and sub:
                sub = Level.objects.filter(id=sub).first()
                post = Document.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), subject=sub).all()
            elif search and not sub:
                post = Document.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search)).all()
            else:
                sub = Level.objects.filter(id=sub).first()
                post = Document.objects.filter(
                    subject=sub).all()
        else:
            post = Document.objects.filter().all()
        c2 = True
        context = {"documents": post, "subjects": subject, "check2": c2}
    else:
        return redirect("check")
    return render(request, "document/list.html", context)


def staff_post_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "GET":
            search = request.GET.get("search")
            # topic = request.GET.get("topic")
            if search:
                post = Post.objects.filter(
                    Q(content__icontains=search)).all()
            else:
                post = Post.objects.all()
        else:
            post = Post.objects.all()
        c2 = True
        context = {"posts": post[::-1], "check2": c2}
    else:
        return redirect("check")
    return render(request, "post/list.html", context)


def staff_document_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        c2 = True
        post = Document.objects.filter(id=id).first()
        context = {"post": post, "check2": c2}
    else:
        return redirect("check")
    return render(request, "document/view.html", context)


def change_status_post(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post.objects.filter(id=id).first()
        if post:
            if request.method == "POST":
                status = request.POST.get("status")

                post.status = status
                post.save()
                return redirect("post_staff_view", id=id)
        else:
            return redirect("my_writting_workspace")
    else:
        return redirect("check")


def change_status_document(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        bio = Bio.objects.filter(user=request.user).first()
        post = Document.objects.filter(id=id).first()
        if post:
            if request.method == "POST":
                status = request.POST.get("status")

                post.status = status
                post.save()
                return redirect("document_staff_list_view", id=id)
        else:
            return redirect("my_writting_workspace")
    else:
        return redirect("check")


def improve_writting(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        result = Writting_result.objects.filter(user=bio).last()
        if result:
            improve = Writting_improve(
                review=result.review).replace("\n", "<br>")
        else:
            improve = "Chúng tôi không có căn cứ để đánh giá khả năng của bạn. Hãy thử làm một vài bài tập và chúng tôi sẽ giúp bạn đánh giá và cải thiện kỹ năng."
        context = {"bio": bio, "improve": improve, "skill": "Writting"}
    else:
        return redirect("check")
    return render(request, "user/improve.html", context=context)


def improve_speaking(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        result = Speaking_scripts_result.objects.filter(user=bio).last()
        if result:
            improve = Speaking_improve(
                review=result.review).replace("\n", "<br>")
        else:
            improve = "Chúng tôi không có căn cứ để đánh giá khả năng của bạn. Hãy thử làm một vài bài tập và chúng tôi sẽ giúp bạn đánh giá và cải thiện kỹ năng."
        context = {"bio": bio, "improve": improve, "skill": "Speaking"}
    else:
        return redirect("check")
    return render(request, "user/improve.html", context=context)


def improve_reading(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        result = Reading_result.objects.filter(user=bio).all()
        result = result[::-1]
        if result:
            review = ""
            if len(result) < 5:
                for i in result:
                    review += str(i.status)+", "
            else:
                for i in range(5):
                    review += str(result[i].status)+", "
            improve = Reading_improve(review=review).replace("\n", "<br>")
        else:
            improve = "Chúng tôi không có căn cứ để đánh giá khả năng của bạn. Hãy thử làm một vài bài tập và chúng tôi sẽ giúp bạn đánh giá và cải thiện kỹ năng."
        context = {"bio": bio, "improve": improve, "skill": "Speaking"}
    else:
        return redirect("check")
    return render(request, "user/improve.html", context=context)


def improve_listening(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        result = Listening_result.objects.filter(user=bio).all()
        result = result[::-1]
        if result:
            review = ""
            if len(result) < 5:
                for i in result:
                    review += str(i.status)+", "
            else:
                for i in range(5):
                    review += str(result[i].status)+", "
            improve = Listening_improve(review=review).replace("\n", "<br>")
        else:
            improve = "Chúng tôi không có căn cứ để đánh giá khả năng của bạn. Hãy thử làm một vài bài tập và chúng tôi sẽ giúp bạn đánh giá và cải thiện kỹ năng."
        context = {"bio": bio, "improve": improve, "skill": "Speaking"}
    else:
        return redirect("check")
    return render(request, "user/improve.html", context=context)
