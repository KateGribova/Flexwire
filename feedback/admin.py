from django.contrib import admin

from feedback import models


class FeedbackTextInline(admin.TabularInline):
    model = models.FeedbackText
    readonly_fields = ('text',)


class FeedbackFilesInline(admin.TabularInline):
    model = models.FeedbackFiles
    readonly_fields = ('files',)


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        models.Feedback.mail.field.name,
        models.Feedback.status.field.name,
    )
    inlines = [
        FeedbackTextInline,
        FeedbackFilesInline,
    ]
