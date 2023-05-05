from django.contrib import admin
from .models import User, Question, QuestionCategory, UserAnswer

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(QuestionCategory)
admin.site.register(UserAnswer)