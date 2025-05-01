from django.test import Client
from django.test import TestCase
from django.urls import reverse


class StaticUrlsTests(TestCase):
    def test_feedback_endpoint(self):
        response = Client().get(reverse('feedback:feedback'))
        self.assertEqual(response.status_code, 200)
