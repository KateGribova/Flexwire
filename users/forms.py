from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from teams.forms import LanguagesWidget
from teams.forms import TechnologyWidget
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = (
            CustomUser.username.field.name,
            CustomUser.email.field.name,
        )


class UserAccountForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    password = None

    class Meta:
        model = CustomUser
        fields = [
            CustomUser.email.field.name,
            CustomUser.first_name.field.name,
            CustomUser.last_name.field.name,
            CustomUser.nickname.field.name,
            CustomUser.about_me.field.name,
            CustomUser.github.field.name,
            CustomUser.contact_data.field.name,
            CustomUser.city.field.name,
            CustomUser.resume.field.name,
            CustomUser.languages.field.name,
            CustomUser.technologies.field.name,
            CustomUser.education_choose.field.name,
            CustomUser.education.field.name,
            CustomUser.image.field.name,
        ]

        widgets = {
            CustomUser.technologies.field.name: TechnologyWidget,
            CustomUser.languages.field.name: LanguagesWidget,
            CustomUser.about_me.field.name: forms.CharField(
                widget=CKEditorWidget()
            ),
        }
