from django.contrib import admin

from . import models


class QuestionAdminInline(admin.TabularInline):
    model = models.Question


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionAdminInline]


class AnswerAdminInline(admin.TabularInline):
    model = models.Answer


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "__str__")
    inlines = [AnswerAdminInline]
    list_filter = ("test",)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserAnswers)
class UserAnswersAdmin(admin.ModelAdmin):
    pass
