from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    language = models.CharField(
        verbose_name='language',
        help_text='Specify communication language',
        max_length=255,
    )

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = 'language'
        verbose_name_plural = 'languages'


class Technology(models.Model):
    technology = models.CharField(
        verbose_name='technology',
        help_text='Specify technology',
        max_length=255,
    )

    def __str__(self):
        return self.technology

    class Meta:
        verbose_name = 'technology'
        verbose_name_plural = 'technologies'


class CustomUser(AbstractUser):
    nickname = models.CharField(
        verbose_name='your nickname',
        help_text='Name that other users will see',
        max_length=255,
    )
    about_me = RichTextField(
        verbose_name='tell more about yourself',
        help_text='Mention everything you consider to be important',
        max_length=2000,
        null=True,
        blank=True,
    )
    github = models.CharField(
        verbose_name='gitHub, Bitbucket or something similar',
        help_text='Specify website to allow others check your projects',
        max_length=255,
    )
    contact_data = models.CharField(
        verbose_name='contact information',
        help_text='Let other users contact you',
        max_length=255,
    )
    city = models.CharField(
        verbose_name='place where you live (country and city)',
        help_text='Specify your country and '
        'city to help people living nearby find you',
        max_length=255,
        blank=True,
        null=True,
    )
    resume = models.FileField(
        verbose_name='resume',
        help_text='Show others your resume',
        blank=True,
        null=True,
        upload_to='resumes/',
    )
    languages = models.ManyToManyField(
        Language,
        verbose_name='languages you speak',
        help_text='Specify languages you know',
    )
    technologies = models.ManyToManyField(
        Technology,
        verbose_name='technologies you use',
        help_text='Specify your stack of technologies',
    )
    image = models.ImageField(
        verbose_name='avatar',
        help_text='Your avatar',
        blank=True,
        null=True,
        upload_to='user_avatars/',
    )

    class EducationChoices(models.TextChoices):
        SCHOOL = 'school', _('School')
        UNIVERSITY = 'university', _('University')

    education_choose = models.CharField(
        verbose_name='education',
        help_text='Select place where you have studied',
        max_length=255,
        choices=EducationChoices.choices,
    )
    education = models.CharField(
        verbose_name='where have you learned?',
        help_text='University you attend or completed',
        max_length=255,
        null=True,
        blank=True,
    )
    user_picture = models.ImageField(
        verbose_name='user picture',
        help_text='Show others yourself',
        null=True,
        blank=True,
        upload_to='user_pictures',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.nickname:
            self.nickname = super().username
