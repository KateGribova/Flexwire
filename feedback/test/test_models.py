from django.test import TestCase

from feedback.models import Feedback
from feedback.models import FeedbackFiles
from feedback.models import FeedbackText


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.feedback = Feedback.objects.create(
            mail='test.test@test.test',
        )
        super().setUpTestData()

    def tearDown(self):
        Feedback.objects.all().delete()
        super().tearDown()

    def test_feedback_model(self):
        feedback_count = Feedback.objects.count()

        user_feedback = Feedback(
            mail='test.test@test.test',
        )
        user_feedback.full_clean()
        user_feedback.save()

        self.assertEqual(Feedback.objects.count(), feedback_count + 1)

    def test_feedback_text_model(self):
        feedback_text_count = FeedbackText.objects.count()

        user_feedback_text = FeedbackText(
            feedback=self.feedback,
            text='test',
        )
        user_feedback_text.full_clean()
        user_feedback_text.save()

        self.assertEqual(FeedbackText.objects.count(), feedback_text_count + 1)

    def test_feedback_files_model(self):
        feedback_files_count = FeedbackFiles.objects.count()

        user_feedback_files = FeedbackFiles(
            feedback=self.feedback,
            files='test.txt',
        )
        user_feedback_files.full_clean()
        user_feedback_files.save()

        self.assertEqual(
            FeedbackFiles.objects.count(), feedback_files_count + 1
        )
