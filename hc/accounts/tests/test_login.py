from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        """ Test login link is sent"""
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        # user count before
        self.user_count_before = User.objects.count()

        # New user using email login
        form = {"email": "oliver@example.org"}
        response = self.client.post("/accounts/login/", form)
        self.assertEqual(response.status_code, 302)

        # user count after
        self.user_count_after = User.objects.count()

        # check if user count increased by 1
        self.assertEqual(self.user_count_before + 1, self.user_count_after)

        # check if email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        self.assertIn(
            "To log into healthchecks.io, please open the link below:",
            mail.outbox[0].body)

        user = User.objects.get(email="oliver@example.org")

        # Assert that check is associated with the new user
        check = Check.objects.get(user=user)
        self.assertEqual(check.user, user)

    def test_it_pops_bad_link_from_session(self):
        """ Test bad link"""
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        self.assertNotIn("bad_link", self.client.session)
