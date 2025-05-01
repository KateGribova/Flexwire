from django.contrib import admin

from users import models

admin.site.register(models.Language)
admin.site.register(models.Technology)


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        models.CustomUser.id.field.name,
        models.CustomUser.username.field.name,
        models.CustomUser.nickname.field.name,
        models.CustomUser.email.field.name,
    )
    list_display_links = (models.CustomUser.username.field.name,)
    filter_horizontal = (
        models.CustomUser.languages.field.name,
        models.CustomUser.technologies.field.name,
    )
    readonly_fields = (models.CustomUser.password.field.name,)
