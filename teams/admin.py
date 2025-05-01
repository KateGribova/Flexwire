from django.contrib import admin

from teams import models

admin.site.register(models.Role)
admin.site.register(models.RoleTeam)


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        models.Team.id.field.name,
        models.Team.title.field.name,
        models.Team.creator.field.name,
        models.Team.is_published.field.name,
    )
    list_display_links = (models.Team.title.field.name,)
    list_editable = (models.Team.is_published.field.name,)
    filter_horizontal = (models.Team.technologies.field.name,)


@admin.register(models.Member)
class MembersAdmin(admin.ModelAdmin):
    list_display = (
        models.Member.id.field.name,
        models.Member.role_team.field.name,
        models.Member.user.field.name,
    )
    list_display_links = (
        models.Member.id.field.name,
        models.Member.role_team.field.name,
    )


@admin.register(models.Pending)
class PendingAdmin(admin.ModelAdmin):
    list_display = (
        models.Pending.id.field.name,
        models.Pending.role_team.field.name,
        models.Pending.user.field.name,
    )
    list_display_links = (
        models.Pending.id.field.name,
        models.Pending.role_team.field.name,
    )
