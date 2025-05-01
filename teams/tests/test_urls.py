from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

import teams.models
import users.models


class StaticUrlTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = users.models.CustomUser.objects.create(
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
        )
        lang = users.models.Language.objects.create(language='eng')
        cls.team = teams.models.Team.objects.create(
            title='team',
            description='desc',
            creator=cls.user,
            is_published=True,
            language=lang,
        )

        cls.dummy_user1 = users.models.CustomUser.objects.create_user(
            username='member',
            password='pwd123qwe',
            email='2@gmail.com',
            nickname='dummy member',
        )
        cls.dummy_user2 = users.models.CustomUser.objects.create_user(
            username='pending',
            password='pwd123qwe',
            email='3@gmail.com',
            nickname='dummy pending',
        )

        role = teams.models.Role.objects.create(name='backend')
        role_team = teams.models.RoleTeam.objects.create(
            team=cls.team, role_default=role
        )
        cls.vacancy = teams.models.RoleTeam.objects.create(
            team=cls.team, role_default=role
        )

        cls.member = teams.models.Member.objects.create(
            role_team=role_team,
            user=cls.dummy_user1,
        )
        cls.pending = teams.models.Pending.objects.create(
            role_team=cls.vacancy, user=cls.dummy_user2
        )

    def tearDown(self):
        users.models.CustomUser.objects.all().delete()
        users.models.Language.objects.all().delete()
        teams.models.Team.objects.all().delete()
        teams.models.RoleTeam.objects.all().delete()
        teams.models.Member.objects.all().delete()
        teams.models.Pending.objects.all().delete()

    def test_access_team_detail(self):
        self.client.force_login(self.user)

        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        control_panel = {
            'Public view': [],
            'Edit': [],
            'Pendings': [],
        }
        info_panel = {
            'About project': [
                self.team.title,
                self.team.description,
                self.team.language.language,
            ],
            'Team': [
                self.member.user.nickname,
                self.member.role_team.role_default.name,
            ],
            'Vacancies': [
                'You are not able to respond to vacancy',
                self.vacancy.role_default.name,
            ],
        }
        for testsuite in (info_panel, control_panel):
            for key, lst in testsuite.items():
                with self.subTest(f'team detail should contain "{key}"'):
                    self.assertContains(resp, key)
                for content in lst:
                    with self.subTest(
                        f'team "{key}" should contain' f' "{content}"'
                    ):
                        self.assertContains(resp, content)

    def test_team_published(self):
        self.team.is_published = False
        self.team.save()

        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertEqual(resp.status_code, 404)

        self.client.force_login(self.dummy_user1)
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertEqual(resp.status_code, 200)

    def test_team_pending(self):
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertContains(resp, self.pending.role_team.role_default.name)

        self.client.force_login(self.pending.user)
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertContains(resp, 'Oops... there is no job for you')

    def test_team_member(self):
        self.client.force_login(self.member.user)
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertContains(resp, 'Oops... there is no job for you')

    def test_team_unauth(self):
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertContains(resp, 'You are not able to respond to vacancy')

    @parameterized.expand([('teams:edit_team',), ('teams:pendings_team',)])
    def test_team_creator_pages(self, view):
        resp = self.client.get(
            reverse(view, kwargs={'pk': self.team.id}), follow=True
        )
        self.assertRedirects(
            resp, reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
