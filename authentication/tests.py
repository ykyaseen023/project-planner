from django.test import TestCase

from .models import RoleChoices, profile


class AuthenticationFlowTests(TestCase):
    def test_login_page_renders_empty_credential_fields(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertNotContains(response, 'value=')

    def test_registered_user_can_log_in(self):
        registration = self.client.post(
            '/api/auth/register/',
            {
                'first_name': 'Planner User',
                'username': 'planner.user@example.com',
                'role': RoleChoices.DEVELOPER,
                'password': 'Violet!Plan47Cedar',
            },
            content_type='application/json',
        )

        self.assertEqual(registration.status_code, 201)
        user = profile.objects.get(username='planner.user@example.com')
        self.assertEqual(user.email, user.username)
        self.assertTrue(user.check_password('Violet!Plan47Cedar'))

        login = self.client.post(
            '/api/auth/login/',
            {
                'username': 'planner.user@example.com',
                'password': 'Violet!Plan47Cedar',
            },
            content_type='application/json',
        )

        self.assertEqual(login.status_code, 200)
        self.assertEqual(set(login.json()), {'access', 'refresh'})
