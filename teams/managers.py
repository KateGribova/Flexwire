from django.db import models
from django.db.models import Prefetch
from django.db.models import Q

import teams.models
import users.models


class TeamManager(models.Manager):
    def teams(self, user_id):
        return (
            self.get_queryset()
            .select_related(teams.models.Team.creator.field.name)
            .filter(
                Q(roleteams__members__user_id=user_id)
                | Q(is_published=True)
                | Q(creator_id=user_id)
            )
            .distinct()
        )

    def get_team_list(self, user_id):
        return (
            self.teams(user_id)
            .prefetch_related(
                Prefetch(teams.models.Team.language.field.name),
                Prefetch(teams.models.Team.technologies.field.name),
            )
            .select_related(teams.models.Team.creator.field.name)
            .only(
                f'{teams.models.Team.technologies.field.name}__'
                f'{users.models.Technology.technology.field.name}',
                f'{teams.models.Team.language.field.name}__'
                f'{users.models.Language.language.field.name}',
                teams.models.Team.title.field.name,
                teams.models.Team.description.field.name,
                teams.models.Team.image.field.name,
                f'{teams.models.Team.creator.field.name}'
                f'__{users.models.CustomUser.username.field.name}',
            )
        )

    def get_team_by_pk(self, user_id, team_pk):
        return (
            self.teams(user_id)
            .filter(pk=team_pk)
            .select_related(teams.models.Team.creator.field.name)
            .only(
                teams.models.Team.title.field.name,
                teams.models.Team.description.field.name,
                teams.models.Team.image.field.name,
                teams.models.Team.presentation.field.name,
                teams.models.Team.is_published.field.name,
                f'{teams.models.Team.creator.field.name}'
                f'__{users.models.CustomUser.username.field.name}',
            )
        )


class RoleTeamManager(models.Manager):
    def get_vacancies(self, team_id):
        from teams.models import RoleTeam

        return (
            self.get_queryset()
            .filter(team_id=team_id, members=None)
            .select_related(RoleTeam.role_default.field.name)
            .only(RoleTeam.role_default.field.name, RoleTeam.team.field.name)
        )


class MemberManager(models.Manager):
    def get_members(self, team_id):
        return (
            self.get_queryset()
            .filter(role_team__team_id=team_id)
            .select_related(
                f'{teams.models.Member.role_team.field.name}__'
                f'{teams.models.RoleTeam.role_default.field.name}',
                teams.models.Member.user.field.name,
            )
            .only(
                f'{teams.models.Member.role_team.field.name}__'
                f'{teams.models.RoleTeam.role_default.field.name}',
                f'{teams.models.Member.user.field.name}'
                f'__{users.models.CustomUser.username.field.name}',
                f'{teams.models.Member.user.field.name}'
                f'__{users.models.CustomUser.image.field.name}',
            )
        )


class PendingManager(models.Manager):
    def get_pendings(self, team_id):
        return (
            self.get_queryset()
            .filter(role_team__team_id=team_id, role_team__members=None)
            .select_related(
                f'{teams.models.Pending.role_team.field.name}'
                f'__{teams.models.RoleTeam.role_default.field.name}'
            )
            .only(
                f'{teams.models.Pending.role_team.field.name}__'
                f'{teams.models.RoleTeam.role_default.field.name}',
                f'{teams.models.Pending.user.field.name}'
                f'__{users.models.CustomUser.username.field.name}',
                f'{teams.models.Pending.user.field.name}'
                f'__{users.models.CustomUser.image.field.name}',
            )
        )
