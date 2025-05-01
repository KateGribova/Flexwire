import django.forms
import django_select2.forms

import teams.models
import users.models


class TechnologyWidget(django_select2.forms.ModelSelect2MultipleWidget):
    model = users.models.Technology
    search_fields = (
        f'{users.models.Technology.technology.field.name}__icontains',
    )

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'data-minimum-input-length': 1}
        super().__init__(*args, **kwargs)


class LanguageWidget(django_select2.forms.ModelSelect2Widget):
    model = users.models.Language
    search_fields = (
        f'{users.models.Language.language.field.name}__icontains',
    )


class LanguagesWidget(django_select2.forms.ModelSelect2MultipleWidget):
    model = users.models.Language
    search_fields = (
        f'{users.models.Language.language.field.name}__icontains',
    )


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.widget_type == 'checkbox':
                field.field.widget.attrs['class'] = 'form-check-input'
                field.label_classes = ('form-check-label',)
            elif field.widget_type in (
                'select',
                'selectmultiple',
                'technology',
            ):
                field.field.widget.attrs['class'] = 'w-100'
            else:
                field.field.widget.attrs['class'] = 'form-control'


class CreateRoleTeamForm(BootstrapForm):
    class Meta:
        model = teams.models.RoleTeam
        fields = (teams.models.RoleTeam.role_default.field.name,)
        widgets = {
            teams.models.RoleTeam.role_default.field.name: (
                django_select2.forms.ModelSelect2Widget(
                    model=teams.models.Role,
                    search_fields=[
                        f'{teams.models.Role.name.field.name}__icontains',
                    ],
                )
            )
        }


class TeamForm(BootstrapForm):
    class Meta:
        model = teams.models.Team
        fields = (
            teams.models.Team.image.field.name,
            teams.models.Team.title.field.name,
            teams.models.Team.description.field.name,
            teams.models.Team.presentation.field.name,
            teams.models.Team.is_published.field.name,
            teams.models.Team.technologies.field.name,
            teams.models.Team.language.field.name,
        )

        widgets = {
            teams.models.Team.technologies.field.name: TechnologyWidget,
            teams.models.Team.language.field.name: LanguageWidget,
        }


class SearchForm(BootstrapForm):
    class Meta:
        model = teams.models.Team
        fields = (
            teams.models.Team.technologies.field.name,
            teams.models.Team.language.field.name,
        )
        widgets = {
            teams.models.Team.technologies.field.name: TechnologyWidget,
            teams.models.Team.language.field.name: LanguagesWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[teams.models.Team.technologies.field.name].required = False
        self.fields[teams.models.Team.language.field.name].required = False
