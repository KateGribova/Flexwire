import pathlib

from ckeditor.fields import RichTextField
import django.db.models

from teams import managers
import users.models


class Team(django.db.models.Model):
    objects = managers.TeamManager()

    def get_upload_image(self, filename):
        return (
            pathlib.Path('team_files')
            / pathlib.Path(str(self.creator.id))
            / pathlib.Path(self.title)
            / f'team_image.{filename.split(".")[-1]}'
        )

    def get_upload_presentation(self, filename):
        return (
            pathlib.Path('team_files')
            / pathlib.Path(str(self.creator.id))
            / pathlib.Path(self.title)
            / f'presentation.{filename.split(".")[-1]}'
        )

    title = django.db.models.CharField(
        verbose_name='title',
        help_text='Write title of your project',
        max_length=64,
    )
    description = RichTextField(
        verbose_name='description',
        help_text='Write description of your project',
    )
    image = django.db.models.ImageField(
        verbose_name='image',
        help_text='Load image of your project',
        null=True,
        blank=True,
        upload_to=get_upload_image,
    )
    presentation = django.db.models.FileField(
        verbose_name='presentation',
        help_text='Load presentation of your project',
        null=True,
        blank=True,
        upload_to=get_upload_presentation,
    )
    creator = django.db.models.ForeignKey(
        users.models.CustomUser,
        help_text='Person who came up with this idea of project',
        on_delete=django.db.models.deletion.CASCADE,
    )
    language = django.db.models.ForeignKey(
        users.models.Language,
        help_text='Specify team language',
        on_delete=django.db.models.deletion.CASCADE,
    )
    technologies = django.db.models.ManyToManyField(
        users.models.Technology,
        verbose_name='technologies your team use',
        help_text='Specify technologies your team use',
    )
    is_published = django.db.models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'
        ordering = ['-id']


class Role(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name='name',
        help_text='Choose role name that you need in your project',
        max_length=128,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'


class RoleTeam(django.db.models.Model):
    objects = managers.RoleTeamManager()

    role_default = django.db.models.ForeignKey(
        Role,
        related_name='roles',
        help_text='Role from standard list',
        on_delete=django.db.models.deletion.CASCADE,
    )
    team = django.db.models.ForeignKey(
        Team,
        related_name='roleteams',
        help_text='Choose  your teammate',
        on_delete=django.db.models.deletion.CASCADE,
    )

    def __str__(self):
        return f'{self.role_default.name} in team {self.team.title}'

    class Meta:
        verbose_name = 'role in team'
        verbose_name_plural = 'roles in team'


class Member(django.db.models.Model):
    objects = managers.MemberManager()

    role_team = django.db.models.ForeignKey(
        RoleTeam,
        related_name='members',
        help_text='Choose roles in your project',
        on_delete=django.db.models.deletion.CASCADE,
    )
    user = django.db.models.ForeignKey(
        users.models.CustomUser,
        help_text='User for this role',
        on_delete=django.db.models.deletion.CASCADE,
    )

    def __str__(self):
        return (
            f'{self.user.nickname} {self.role_team.role_default.name}'
            f' {self.role_team.team.title}'
        )

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'


class Pending(django.db.models.Model):
    objects = managers.PendingManager()

    role_team = django.db.models.ForeignKey(
        RoleTeam,
        related_name='pendings',
        help_text='Choose role that you want to be',
        on_delete=django.db.models.deletion.CASCADE,
    )
    user = django.db.models.ForeignKey(
        users.models.CustomUser,
        help_text='User for this pending',
        on_delete=django.db.models.deletion.CASCADE,
    )

    def __str__(self):
        return (
            f'{self.user.nickname} {self.role_team.role_default.name}'
            f' {self.role_team.team.title}'
        )

    class Meta:
        verbose_name = 'pending'
        verbose_name_plural = 'pending list'
