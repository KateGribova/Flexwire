from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import CreateView

from feedback import models
from feedback.forms import FeedbackFilesForm
from feedback.forms import FeedbackForm
from feedback.forms import FeedbackTextForm
from feedback.models import Feedback


class FeedbackView(CreateView):
    model = Feedback
    fields = '__all__'
    template_name = 'feedback/feedback.html'
    success_url = 'feedback:feedback'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedback_form = FeedbackForm()
        feedback_text_form = FeedbackTextForm()
        feedback_file_form = FeedbackFilesForm()
        context.setdefault('feedback_form', feedback_form)
        context.setdefault('feedback_text_form', feedback_text_form)
        context.setdefault('feedback_file_form', feedback_file_form)
        return context

    def post(self, request, *args, **kwargs):
        feedback_form = FeedbackForm(request.POST)
        feedback_text_form = FeedbackTextForm(request.POST)
        feedback_file_form = FeedbackFilesForm(request.POST, request.FILES)

        if (
            feedback_form.is_valid()
            and feedback_text_form.is_valid()
            and feedback_file_form.is_valid()
        ):
            text = feedback_text_form.cleaned_data['text']
            mail = feedback_form.cleaned_data['mail']
            message = (
                'Thank you for your comments and suggestions!\nYou submitted '
                'feedback on the FLEXWIRE website.\nYour feedback '
                'will be certainly forwarded to customer support for '
                'improving our service.\n'
                f'Your Feedback:\n{text}\n\n'
                'We hope you will have a positive '
                'FLEXWIRE site experience\n'
                '---\n'
                'FLEXWIRE'
            )
            send_mail(
                'FLEXWIRE',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [mail],
                fail_silently=False,
            )

            feedback_user = models.Feedback.objects.create(
                mail=mail,
            )
            models.FeedbackText.objects.create(
                feedback=feedback_user,
                text=text,
            )
            for user_file in request.FILES.getlist('files'):
                models.FeedbackFiles.objects.create(
                    feedback=feedback_user,
                    files=user_file,
                )

            messages.add_message(
                request,
                messages.INFO,
                'Your feedback has been sent successfully!',
            )
        return super().post(self, request, *args, **kwargs)
