from django import shortcuts
from django.conf import settings
from django.contrib.auth import mixins
from django.core.mail import send_mail
from django.db import models
from django.views import generic

import teams.forms
import teams.models


class TeamsList(generic.ListView):
    model = teams.models.Team
    template_name = 'teams/teams_list.html'
    paginate_by = 3
    context_object_name = 'teams'

    def get_queryset(self):
        return teams.models.Team.objects.get_team_list(self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = teams.forms.SearchForm()
        return context

    def post(self, request):
        technologies = request.POST.getlist('technologies')
        languages = request.POST.getlist('language')
        search = request.POST.getlist('value')
        form = teams.forms.SearchForm(request.POST)

        query = super().get_queryset()

        if technologies:
            query = query.filter(technologies__id__in=technologies)

        if languages:
            query = query.filter(language_id__in=languages)

        if search:
            search = search[0]
            query = query.filter(
                models.Q(title__icontains=search)
                | models.Q(description__icontains=search)
            )
        self.object_list = query
        return super().render_to_response(
            {'teams': query.all(), 'form': form, 'value': search}
        )


class TeamMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pendings = teams.models.Pending.objects.get_pendings(
            self.kwargs.get('pk')
        )
        team = shortcuts.get_object_or_404(
            teams.models.Team.objects.get_team_by_pk(
                self.request.user.id or -1, self.kwargs.get('pk')
            )
        )
        context.update(
            {
                'pendings': pendings,
                'team': team,
            }
        )
        return context


class TeamDetail(TeamMixin, generic.DetailView):
    model = teams.models.Team
    template_name = 'teams/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = context['team']

        members = teams.models.Member.objects.get_members(team.id).all()
        if not members.filter(user_id=self.request.user.id).exists():
            vacancies = teams.models.RoleTeam.objects.get_vacancies(team.id)
            if self.request.user.is_authenticated:
                vacancies = vacancies.exclude(
                    pendings__user_id=self.request.user.id
                )
        else:
            vacancies = []

        language = team.language
        technologies = team.technologies.all()

        context.update(
            {
                'technologies': technologies,
                'language': language,
                'vacancies': vacancies,
                'members': members,
            }
        )
        return context


class TeamEdit(TeamMixin, generic.TemplateView):
    model = teams.models.Team
    template_name = 'teams/team_edit.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        team = context['team']
        if self.request.user.id != team.creator_id:
            return shortcuts.redirect('teams:team_detail', kwargs.get('pk'))

        context['members'] = teams.models.Member.objects.get_members(team.id)
        context['form'] = teams.forms.TeamForm(instance=team)
        context['roleteams'] = teams.models.RoleTeam.objects.get_vacancies(
            team.id
        )

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        team = context['team']
        if self.request.user.id != team.creator_id:
            return shortcuts.redirect('teams:team_detail', kwargs.get('pk'))

        form = teams.forms.TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return shortcuts.redirect('teams:edit_team', kwargs.get('pk'))
        context['form'] = form
        return self.render_to_response(context)


class TeamPendings(TeamMixin, generic.TemplateView):
    template_name = 'teams/team_pendings.html'

    def get(self, request, *args, **kwargs):
        context = super(TeamPendings, self).get_context_data(**kwargs)
        if request.user != context['team'].creator:
            return shortcuts.redirect('teams:team_detail', kwargs.get('pk'))
        return self.render_to_response(context)


class UserTeams(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'teams/user_teams.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return teams.models.Team.objects.filter(
            models.Q(creator_id=self.request.user.id)
            | models.Q(roleteams__members__id__contains=self.request.user.id)
        ).distinct()


class CreateRoleTeam(generic.CreateView):
    template_name = 'teams/create_roleteam.html'
    form_class = teams.forms.CreateRoleTeamForm

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        team = shortcuts.get_object_or_404(
            teams.models.Team.objects.get_team_by_pk(
                self.request.user.id or -1, kwargs.get('pk')
            )
        )
        if team.creator_id != self.request.user.id:
            return shortcuts.redirect('teams:team_detail', pk)

        form = teams.forms.CreateRoleTeamForm(request.POST)
        role_team = form.save(commit=False)
        role_team.team = team
        role_team.save()
        return shortcuts.redirect('teams:edit_team', pk)


class RemoveRoleTeam(generic.View):
    def post(self, request, pk):
        role_team = shortcuts.get_object_or_404(teams.models.RoleTeam, pk=pk)
        if role_team.team.creator_id != self.request.user.id:
            return shortcuts.redirect('teams:team_detail', role_team.team_id)
        role_team.delete()
        return shortcuts.redirect('teams:edit_team', role_team.team_id)


class CreatePending(mixins.LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        role_team = shortcuts.get_object_or_404(teams.models.RoleTeam, pk=pk)
        is_member = (
            teams.models.Member.objects.get_members(role_team.team_id)
            .filter(user_id=self.request.user.id)
            .exists()
        )
        is_pending = teams.models.Pending.objects.filter(
            user=self.request.user, role_team=role_team
        ).exists()

        if role_team.team.creator_id != self.request.user.id and (
            not is_pending and not is_member
        ):
            teams.models.Pending.objects.create(
                role_team=role_team,
                user=self.request.user,
            )
            send_mail(
                'You created pending to team',
                f'You created pending to team {role_team.team.title}.\n'
                'It will be reviewed shortly by the creator of the team.\n'
                '---\n'
                'FLEXWIRE',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
        return shortcuts.redirect('teams:team_detail', role_team.team_id)


class RemoveMember(generic.View):
    def post(self, request, pk):
        member = shortcuts.get_object_or_404(teams.models.Member, pk=pk)
        if member.role_team.team.creator_id == self.request.user.id:
            member.delete()
            send_mail(
                'You was removed from the team',
                f'Creator of the team {member.role_team.team.title} '
                'has made a decision to remove you from the team.\n'
                '---\n'
                'FLEXWIRE',
                settings.DEFAULT_FROM_EMAIL,
                [member.user.email],
                fail_silently=False,
            )
        return shortcuts.redirect(
            'teams:team_detail', member.role_team.team_id
        )


class AcceptPending(generic.View):
    def post(self, request, pk):
        pending = shortcuts.get_object_or_404(teams.models.Pending, pk=pk)
        if pending.role_team.team.creator_id == self.request.user.id:
            send_mail(
                'Your pending accepted',
                f'Creator of the team {pending.role_team.team.title} '
                'has accepted your pending.\n'
                '---\n'
                'FLEXWIRE',
                settings.DEFAULT_FROM_EMAIL,
                [pending.user.email],
                fail_silently=False,
            )
            pending.delete()
            teams.models.Member.objects.create(
                role_team=pending.role_team, user=pending.user
            )
        return shortcuts.redirect(
            'teams:team_detail', pending.role_team.team_id
        )


class RejectPending(generic.View):
    def post(self, request, pk):
        pending = shortcuts.get_object_or_404(teams.models.Pending, pk=pk)
        if pending.role_team.team.creator_id == self.request.user.id:
            send_mail(
                'Your pending rejected',
                f'Creator of the team {pending.role_team.team.title} '
                'has rejected your pending.\n'
                '---\n'
                'FLEXWIRE',
                settings.DEFAULT_FROM_EMAIL,
                [pending.user.email],
                fail_silently=False,
            )
            pending.delete()
        return shortcuts.redirect(
            'teams:team_detail', pending.role_team.team_id
        )


class CreateTeam(
    mixins.LoginRequiredMixin,
    generic.CreateView,
):
    model = teams.models.Team
    form_class = teams.forms.TeamForm
    template_name = 'teams/create_team.html'

    def form_valid(self, form, *args, **kwargs):
        form.instance.creator = self.request.user
        return super(CreateTeam, self).form_valid(form)

    def get_success_url(self):
        return shortcuts.reverse(
            'teams:team_detail', kwargs={'pk': self.object.pk}
        )
