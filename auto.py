from tin_hoc_tre.models import *
from django.contrib.auth.models import User
from tin_hoc_tre.speakingGPT import *
from tin_hoc_tre.writtingGPT import *
from tin_hoc_tre.readingGPT import *
from tin_hoc_tre.listeningGPT import *
from tin_hoc_tre.listeningAudioMaker import *
import io
from tin_hoc_tre.GPTsecurity import check_document, check_image, check_content
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# from PIL import Image
import requests
import random

'''
def auto_create_user(name, email, superuser=False):
    user = User.objects.filter(email=email).first()
    if user:
        print("You already have an account")
    else:
        thumbnail = requests.get(
            "https://bdt.pythonanywhere.com/media/images/470174170_612846771252973_488254979111110788_n.jpg")
        avatar = requests.get("https://scontent.fhan15-1.fna.fbcdn.net/v/t39.30808-6/473446076_633552985849018_250936394473140360_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeHYHnV-NdhxAAupGig9IsCDHWGnptbCZpkdYaem1sJmmUhKfBYE4cZKf5B4Jf-HgtSJpIW6QFL7MWJDvBoL5Ma_&_nc_ohc=uGtICzmB-NoQ7kNvgEI4YcE&_nc_oc=AdgT4tb2vjSUFv_6C1C8FAnirdkwIDn18QOBtSn0GywWNZAMhKSmM2UUjK7-8x8i1rE&_nc_zt=23&_nc_ht=scontent.fhan15-1.fna&_nc_gid=ANldWS9oBhxy8VRwIqzev7P&oh=00_AYARlesh_ryCJxXjcAC_o1qcPE8l3ovXUjDB37XAOVM8AA&oe=67CCC772")
        if thumbnail.status_code == 200 and avatar.status_code == 200:
            ava = Image.open(io.BytesIO(avatar.content))
            ava_format = ava.format.lower()
            ava_file_name = f'image.{ava_format}'

            theme = Image.open(io.BytesIO(thumbnail.content))
            theme_format = theme.format.lower()
            theme_file_name = f'image.{theme_format}'
        if superuser:
            user = User.objects.create_superuser(
                username=name, email=email, password="12345678")
            user.save()
            bio = Bio(user=user, speaking_score=0,
                      writing_score=0, reading_score=0, grammar_score=0, listening_score=0, avg_score=0)
            bio.save()
            bio.avatar.save(ava_file_name, ContentFile(avatar.content))
            bio.thumbnail.save(theme_file_name, ContentFile(thumbnail.content))
        else:
            user = User.objects.create_user(
                username=name, email=email, password="12345678")
            user.save()
            bio = Bio(user=user, speaking_score=0, writing_score=0,
                      reading_score=0, grammar_score=0, listening_score=0, avg_score=0)
            bio.save()
            bio.avatar.save(ava_file_name, ContentFile(avatar.content))
            bio.thumbnail.save(theme_file_name, ContentFile(thumbnail.content))
        print(f"User:{user.username}, Password:12345678, Admin:{superuser}")


auto_create_user(name="Trường TH, THCS & THPT FPT Bắc Ninh",
                 email="muz71958@jioso.com", superuser=True)
'''
bio = Bio.objects.filter(user__id=2).first()
theme = ["Thể thao", "nhà cửa", "lễ hội", "công việc", "động vật",
         "học tập", "xe cộ", "du lịch", "Nấu ăn", "học tập"]

for i in range(15):
    t_random = random.randint(0, 9)
    l_random = random.randint(1, 6)
    title = f"The listening about {theme[t_random]}"
    level = Level.objects.filter(id=l_random).first()
    sql = Listening(title=title, level=level, status="Công khai", user=bio)
    sql.save()
    scripts = listening_scripts_maker(level=level.name, theme=theme[t_random])
    sql.description = scripts.replace("\n", "<br>")
    sql.save()
    print(sql.description)
    audio_file = text_to_speech_file(text=scripts, id=sql.id)
    response = HttpResponse(content_type='audio/mpeg')
    response['Content-Disposition'] = f'attachment; filename="{sql.id}.mp3"'
    for chunk in audio_file:
        if chunk:
            response.write(chunk)
    file_content = io.BytesIO(response.content)
    sql.audio.save(f'{sql.id}.mp3', ContentFile(file_content.getvalue()))
    sql.save()
    questions = listening_question_maker(essay=scripts, level=level.name)
    a = questions.split("\n")
    print(a)
    for i in a:
        if len(i) > 0:
            sql2 = Listening_question.objects.filter(listening=sql).count()
            sql1 = Listening_question(
                question=i, listening=sql, no_question=sql2+1)
            sql1.save()
    print(f"Successfull created listening no.{sql.id}")
'''
for i in range(10):
    t_random = random.randint(0, 9)
    l_random = random.randint(1, 6)
    level = Level.objects.filter(id=l_random).first()
    
    description1 = reading_maker(level=level.name, theme=theme[t_random])
    title = reading_title_maker(level=level.name, essay=description1)
    description = description1.replace("\n", "<br>")
    print(description)
    sql = Reading(title=title, description=description, user=bio,
                  level=level, status="Công khai")
    sql.save()
    questions = reading_question_maker(
        essay=description1, level=level.name)
    a = questions.split("\n")
    print(a)
    for i in a:
        if len(i) > 0:
            sql2 = Reading_question.objects.filter(reading=sql).count()
            sql1 = Reading_question(
                question=i, reading=sql, no_question=sql2+1)
            sql1.save()
    print(f"Question no.{sql.id} successfully created")
    
    # level = Level.objects.filter(id=level).first()
    title = f"Bài speaking về {theme[t_random]}"
    sql = Speaking_scripts(title=title, description=title, user=bio,
                           level=level, status="Công khai")
    sql.save()

    scripts = speaking_scripts_maker(level=level.name, theme=theme)
    a = scripts.split("\n")
    print(a)
    # b = str(sql.id)+".txt"
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
    print(
        f"done speaking scripts no.{sql.id}, the file is {sql.speaker_script.url}")
    '''
t_random = random.randint(0, 9)
l_random = random.randint(1, 6)
level = Level.objects.filter(id=l_random).first()
scripts = listening_scripts_maker(level=level.name, theme=theme[t_random])
print(scripts)
