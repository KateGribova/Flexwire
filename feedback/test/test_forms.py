from django.test import Client
from django.test import TestCase
from django.urls import reverse

from feedback.forms import FeedbackFilesForm
from feedback.forms import FeedbackForm
from feedback.forms import FeedbackTextForm


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()
        cls.text_form = FeedbackTextForm()
        cls.files_form = FeedbackFilesForm()

    def test_feedback_text_label(self):
        text_label = self.text_form.fields['text'].label
        self.assertEqual(text_label, 'Feedback')

    def test_feedback_mail_label(self):
        mail_label = self.form.fields['mail'].label
        self.assertEqual(mail_label, 'Mail')

    def test_feedback_files_label(self):
        files_label = self.files_form.fields['files'].label
        self.assertEqual(files_label, 'Files')

    def test_feedback_text_help_text(self):
        text_label = self.text_form.fields['text'].help_text
        self.assertEqual(text_label, 'Write feedback to our site')

    def test_feedback_mail_help_text(self):
        mail_help_text = self.form.fields['mail'].help_text
        self.assertEqual(mail_help_text, 'Write your email')

    def test_feedback_files_help_text(self):
        files_help_text = self.files_form.fields['files'].help_text
        self.assertEqual(files_help_text, 'Load additional files')

    def test_feedback_create_task(self):
        form_data = {
            'mail': 'test.test@test.test',
        }

        response = Client().post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertIn('feedback_form', response.context)
        self.assertIn('feedback_text_form', response.context)
        self.assertIn('feedback_file_form', response.context)
