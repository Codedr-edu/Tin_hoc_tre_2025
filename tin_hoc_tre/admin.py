from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Bio)
admin.site.register(Level)
admin.site.register(Emoji)
admin.site.register(Speaking_scripts)
admin.site.register(Speaking_scripts_comment)
admin.site.register(Speaking_scripts_result)
admin.site.register(Speaking_scripts_emoji)
admin.site.register(Writting)
admin.site.register(Writting_comment)
admin.site.register(Writting_result)
admin.site.register(Writting_emoji)
admin.site.register(Reading)
admin.site.register(Reading_comment)
admin.site.register(Reading_result)
admin.site.register(Reading_emoji)
admin.site.register(Listening)
admin.site.register(Listening_question)
admin.site.register(Listening_comment)
admin.site.register(Listening_result)
admin.site.register(Listening_emoji)
