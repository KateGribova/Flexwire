from django.core import exceptions
from django.test import TestCase

from users.models import CustomUser
from users.models import Language
from users.models import Technology


class TestDataBaseAddUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.technology = Technology.objects.create(
            id=1,
            technology='technology',
        )
        cls.language = Language.objects.create(
            id=1,
            language='language',
        )

    def tearDown(self):
        super().tearDown()
        CustomUser.objects.all().delete()
        Language.objects.all().delete()
        Technology.objects.all().delete()

    def test_unable_create_user_without_github(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                contact_data='https://t.me/some_user',
                education_choose='university',
                education='some university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_unable_create_user_without_contact_data(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                github='https://github.com/some_user',
                education_choose='university',
                education='some university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_unable_create_user_without_education_choose(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                github='https://github.com/some_user',
                contact_data='https://t.me/some_user',
                education='some university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_unable_create_user_without_education(self):
        user_count = CustomUser.objects.count()

        with self.assertRaises(exceptions.ValidationError):
            self.user = CustomUser(
                id=1,
                username='username',
                email='1@gmail.com',
                nickname='nickname',
                github='https://github.com/some_user',
                contact_data='https://t.me/some_user',
                education_choose='university',
            )

            self.user.full_clean()
            self.user.save()

            self.user.technologies.add(TestDataBaseAddUser.technology)
            self.user.languages.add(TestDataBaseAddUser.language)

            self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count)

    def test_able_create_user_with_only_necessary_fields(self):
        user_count = CustomUser.objects.count()

        self.user = CustomUser(
            id=1,
            username='username',
            email='1@gmail.com',
            nickname='nickname',
            github='https://github.com/some_user',
            contact_data='https://t.me/some_user',
            education_choose='university',
            education='some university',
        )

        self.user.set_password('password')

        self.user.full_clean()
        self.user.save()

        self.user.technologies.add(TestDataBaseAddUser.technology)
        self.user.languages.add(TestDataBaseAddUser.language)

        self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count + 1)

    def test_able_create_user_with_all_fields(self):
        user_count = CustomUser.objects.count()

        self.user = CustomUser(
            id=1,
            username='username',
            email='1@gmail.com',
            nickname='nickname',
            about_me='some info',
            github='https://github.com/some_user',
            contact_data='https://t.me/some_user',
            city='Karaganda',
            resume='some_resume.pfd',
            education_choose='university',
            education='some university',
            user_picture='avatar.jpg',
        )

        self.user.set_password('password')

        self.user.full_clean()
        self.user.save()

        self.user.technologies.add(TestDataBaseAddUser.technology)
        self.user.languages.add(TestDataBaseAddUser.language)

        self.user.save()

        self.assertEqual(CustomUser.objects.count(), user_count + 1)
