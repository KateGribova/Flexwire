from django.db import models
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    created_on = models.DateTimeField(
        verbose_name='date of writing',
        auto_now_add=True,
    )
    mail = models.EmailField(
        verbose_name='mail',
        help_text='Write your email',
        default='user_mail@example.com',
    )

    class Status(models.TextChoices):
        GOT = 'got', _('Got')
        IN_PROGRESS = 'in progress', _('In progress')
        ANSWER_GIVEN = 'answered', _('Answered')

    status = models.CharField(
        verbose_name='status',
        help_text='Choose application status',
        max_length=11,
        choices=Status.choices,
        default=Status.GOT,
    )

    def __str__(self):
        return 'Feedback №' + str(self.pk)

    class Meta:
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'


class FeedbackFiles(models.Model):
    def saving_path(self, filename):
        return 'uploads/{0}/{1}'.format(self.feedback.pk, filename)

    files = models.FileField(
        verbose_name='files',
        help_text='Load additional files',
        upload_to=saving_path,
        null=True,
        default=None,
    )
    feedback = models.ForeignKey(
        Feedback,
        verbose_name='files',
        help_text='Load files',
        on_delete=models.CASCADE,
        default=None,
    )

    def __str__(self):
        return self.files.name

    class Meta:
        verbose_name = 'feedback file'
        verbose_name_plural = 'feedback files'


class FeedbackText(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name='text',
        help_text='Write your feedback',
        primary_key=True,
    )
    text = models.TextField(
        verbose_name='feedback',
        help_text='Write feedback to our site',
        null=True,
        blank=True,
    )

    def __str__(self):
        return 'Feedback text №' + str(self.feedback.pk)

    class Meta:
        verbose_name = 'feedback text'
        verbose_name_plural = 'feedback texts'
