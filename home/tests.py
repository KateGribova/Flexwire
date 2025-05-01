import django.shortcuts
import django.test


class StaticUrlTest(django.test.TestCase):
    def test_landing(self):
        response = django.test.Client().get(
            django.shortcuts.reverse('home:landing')
        )
        self.assertEqual(response.status_code, 200)
