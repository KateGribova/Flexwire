from io import BytesIO

from django.conf import settings
from django.core import mail
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from teams.models import Member
from teams.models import Pending
from teams.models import Role
from teams.models import RoleTeam
from teams.models import Team
from users.models import CustomUser
from users.models import Language
from users.models import Technology


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        technology = Technology.objects.create(
            id=1,
            technology='technology',
        )
        language = Language.objects.create(
            id=1,
            language='language',
        )
        cls.user_creator = CustomUser.objects.create(
            id=1,
            username='creator',
            password='testpassword',
            email='test1@test.test',
            nickname='creator',
            contact_data='https://t.me/test1',
            education_choose='university',
            education='test university 1',
        )
        cls.user_member = CustomUser.objects.create(
            id=2,
            username='member',
            password='testpassword',
            email='test2@test.test',
            nickname='member',
            contact_data='https://t.me/test2',
            education_choose='university',
            education='test university 2',
        )
        cls.user_not_member = CustomUser.objects.create(
            id=3,
            username='notmember',
            password='testpassword',
            email='test3@test.test',
            nickname='notmember',
            contact_data='https://t.me/test3',
            education_choose='university',
            education='test university 3',
        )
        cls.user_pending = CustomUser.objects.create(
            id=4,
            username='pending',
            password='testpassword',
            email='test4@test.test',
            nickname='pending',
            contact_data='https://t.me/test4',
            education_choose='university',
            education='test university 4',
        )
        ViewTests.user_creator.technologies.add(technology)
        ViewTests.user_creator.languages.add(language)
        ViewTests.user_member.technologies.add(technology)
        ViewTests.user_member.languages.add(language)
        ViewTests.user_not_member.technologies.add(technology)
        ViewTests.user_not_member.languages.add(language)
        cls.team = Team.objects.create(
            title='Test title',
            description='Test description',
            language=language,
            creator=ViewTests.user_creator,
            is_published=True,
        )
        role = Role.objects.create(name='test role name')
        cls.role_team = RoleTeam.objects.create(
            role_default=role,
            team=ViewTests.team,
        )
        cls.pending_role_team = RoleTeam.objects.create(
            role_default=role,
            team=ViewTests.team,
        )
        cls.member = Member.objects.create(
            role_team=ViewTests.role_team, user=ViewTests.user_member
        )
        cls.pending = Pending.objects.create(
            role_team=ViewTests.pending_role_team, user=ViewTests.user_pending
        )

    def tearDown(self):
        super().tearDown()
        CustomUser.objects.all().delete()
        Team.objects.all().delete()
        Member.objects.all().delete()
        RoleTeam.objects.all().delete()
        Role.objects.all().delete()
        Technology.objects.all().delete()
        Language.objects.all().delete()
        Pending.objects.all().delete()

    def test_remove_member_deleting_member(self):
        client = Client()
        client.force_login(self.user_creator)
        client.post(reverse('teams:remove_member', args=[1]))

        self.assertFalse(Member.objects.filter(pk=1).exists())

    def test_remove_member_status_code(self):
        client = Client()
        client.force_login(self.user_creator)
        response = client.post(reverse('teams:remove_member', args=[1]))

        self.assertEqual(response.status_code, 302)

    def test_remove_member_send_mail(self):
        client = Client()
        client.force_login(self.user_creator)
        client.post(reverse('teams:remove_member', args=[1]))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, 'You was removed from the team'
        )
        self.assertEqual(
            mail.outbox[0].body,
            'Creator of the team Test title has made a decision to remove you '
            'from the team.\n'
            '---\n'
            'FLEXWIRE',
        )
        self.assertEqual(
            mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL
        )
        self.assertEqual(mail.outbox[0].to, [self.user_member.email])

    def test_create_pending_send_mail(self):
        client = Client()
        client.force_login(self.user_not_member)
        client.post(reverse('teams:create_pending', args=[1]))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You created pending to team')
        self.assertEqual(
            mail.outbox[0].body,
            'You created pending to team Test title.\n'
            'It will be reviewed shortly by the creator of the team.\n'
            '---\n'
            'FLEXWIRE',
        )
        self.assertEqual(
            mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL
        )
        self.assertEqual(mail.outbox[0].to, [self.user_not_member.email])

    def test_accept_pending_send_mail(self):
        Pending.objects.create(
            role_team=self.role_team,
            user=self.user_not_member,
        )

        client = Client()
        client.force_login(self.user_creator)
        client.post(
            reverse(
                'teams:accept_pending',
                args=[self.role_team.pendings.first().id],
            )
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your pending accepted')
        self.assertEqual(
            mail.outbox[0].body,
            'Creator of the team Test title '
            'has accepted your pending.\n'
            '---\n'
            'FLEXWIRE',
        )
        self.assertEqual(
            mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL
        )
        self.assertEqual(mail.outbox[0].to, [self.user_not_member.email])

    def test_reject_pending_send_mail(self):
        Pending.objects.create(
            role_team=self.role_team,
            user=self.user_not_member,
        )

        client = Client()
        client.force_login(self.user_creator)
        client.post(
            reverse(
                'teams:reject_pending',
                args=[self.role_team.pendings.first().id],
            )
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your pending rejected')
        self.assertEqual(
            mail.outbox[0].body,
            'Creator of the team Test title '
            'has rejected your pending.\n'
            '---\n'
            'FLEXWIRE',
        )
        self.assertEqual(
            mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL
        )
        self.assertEqual(mail.outbox[0].to, [self.user_not_member.email])

    def test_post_unauth(self):
        resp = self.client.post(
            reverse('teams:edit_team', kwargs={'pk': 1}),
            data={},
            follow=True,
        )
        self.assertRedirects(
            resp, reverse('teams:team_detail', kwargs={'pk': 1})
        )

    def test_post_user(self):
        self.client.force_login(self.user_not_member)
        resp = self.client.post(
            reverse('teams:edit_team', kwargs={'pk': 1}),
            data={},
            follow=True,
        )
        self.assertRedirects(
            resp, reverse('teams:team_detail', kwargs={'pk': 1})
        )

    def test_post_member(self):
        self.client.force_login(self.user_member)
        resp = self.client.post(
            reverse('teams:edit_team', kwargs={'pk': 1}),
            data={},
            follow=True,
        )
        self.assertRedirects(
            resp, reverse('teams:team_detail', kwargs={'pk': 1})
        )

    def test_unauth_create_pending(self):
        pendings_count = self.role_team.pendings.count()
        url = reverse('teams:create_pending', kwargs={'pk': self.role_team.id})
        resp = self.client.post(url, follow=True)
        self.assertRedirects(resp, f'{reverse("users:login")}?next={url}')
        self.assertEqual(pendings_count, self.role_team.pendings.count())

    def test_create_pending(self):
        users = [self.user_member, self.user_creator]
        for user in users:
            self.client.force_login(user)
            pendings_count = self.role_team.pendings.count()
            self.client.post(
                reverse(
                    'teams:create_pending', kwargs={'pk': self.role_team.id}
                ),
                follow=True,
            )
            with self.subTest('This user must not be able to create pending'):
                self.assertEqual(
                    pendings_count, self.role_team.pendings.count()
                )

    def test_accept_pending_wrong(self):
        users = [None, self.user_member]

        for user in users:
            if user:
                self.client.force_login(user)
            members_count = self.role_team.members.count()
            pendings_count = self.role_team.pendings.count()
            self.client.post(
                reverse(
                    'teams:accept_pending', kwargs={'pk': self.pending.id}
                ),
                follow=True,
            )
            with self.subTest('This user must not be able to accept pending'):
                self.assertEqual(
                    pendings_count, self.role_team.pendings.count()
                )
                self.assertEqual(members_count, self.role_team.members.count())

    def test_reject_pending_wrong(self):
        users = [None, self.user_member]

        for user in users:
            if user:
                self.client.force_login(user)
            members_count = self.role_team.members.count()
            pendings_count = self.role_team.pendings.count()
            self.client.post(
                reverse(
                    'teams:reject_pending', kwargs={'pk': self.pending.id}
                ),
                follow=True,
            )
            with self.subTest('This user must not be able to accept pending'):
                self.assertEqual(
                    pendings_count, self.role_team.pendings.count()
                )
                self.assertEqual(members_count, self.role_team.members.count())

    def test_accept_pending(self):
        self.client.force_login(self.user_creator)
        members_count = self.pending_role_team.members.count()
        pendings_count = self.pending_role_team.pendings.count()

        self.client.post(
            reverse('teams:accept_pending', kwargs={'pk': self.pending.id}),
            follow=True,
        )
        self.assertEqual(
            pendings_count - 1, self.pending_role_team.pendings.count()
        )
        self.assertEqual(
            members_count + 1, self.pending_role_team.members.count()
        )

    def test_reject_pending(self):
        self.client.force_login(self.user_creator)
        members_count = self.pending_role_team.members.count()
        pendings_count = self.pending_role_team.pendings.count()

        self.client.post(
            reverse('teams:reject_pending', kwargs={'pk': self.pending.id}),
            follow=True,
        )
        self.assertEqual(
            pendings_count - 1, self.pending_role_team.pendings.count()
        )
        self.assertEqual(members_count, self.pending_role_team.members.count())

    def test_corrupted_image(self):
        self.client.force_login(self.user_creator)
        image = BytesIO(b'image otve4ayu')
        image.name = 'image.pdf'
        form = {
            'title': 'title',
            'description': 'title',
            'language': '1',
            'technologies': ['1'],
            'image': image,
        }
        resp = self.client.post(
            reverse('teams:edit_team', kwargs={'pk': self.team.id}),
            data=form,
        )
        self.assertContains(
            resp,
            'Upload a valid image. The file you uploaded was either not an '
            'image or a corrupted image.',
        )

    def test_adding_presentation(self):
        self.client.force_login(self.user_creator)
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertNotContains(resp, 'Presentation')

        pres = BytesIO(b'presentation')
        pres.name = 'perf.pdf'
        form = {
            'title': 'title',
            'description': 'title',
            'language': '1',
            'technologies': ['1'],
            'presentation': pres,
        }
        self.client.post(
            reverse('teams:edit_team', kwargs={'pk': self.team.id}),
            data=form,
            follow=True,
        )
        resp = self.client.get(
            reverse('teams:team_detail', kwargs={'pk': self.team.id})
        )
        self.assertContains(resp, 'Presentation')
