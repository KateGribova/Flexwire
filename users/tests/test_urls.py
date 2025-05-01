from django.test import Client
from django.test import TestCase
from django.urls import reverse
import parameterized.parameterized


class StaticUrlsTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ('login', 200),
            ('password_reset', 200),
            ('password_reset_complete', 200),
            ('password_reset_done', 200),
            ('signup', 200),
            ('logout', 302),
            ('password_change', 302),
            ('password_change_done', 302),
        ]
    )
    def test_registration_endpoints(self, url, status):
        response = Client().get(reverse(f'users:{url}'))
        self.assertEqual(response.status_code, status)

    def test_password_reset_confirm_endpoint(self):
        response = Client().get(
            reverse(
                'users:password_reset_confirm',
                args=('Mg', 'bm573d-62e40259727921f3b2b46c36f31ccf78'),
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_activate_user_endpoint(self):
        response = Client().get(
            reverse(
                'users:activate_user',
                args=('bm573d-62e40259727921f3b2b46c36f31ccf78',),
            )
        )
        self.assertEqual(response.status_code, 200)
