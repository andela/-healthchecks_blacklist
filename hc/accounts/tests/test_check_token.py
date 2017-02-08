from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase
from django.urls import reverse

class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        """ Test response for login"""
        response = self.client.get(reverse("hc-check-token", args =["alice", "secret-token"]))
        self.assertContains(response, "You are about to log in")

    def test_it_redirects(self):
        """ Test redirection correct login and token"""

        response = self.client.post(
            "/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_login_and_redirects_already_logged_in(self):
        """ Login and test it redirects already logged in"""
        payload = {"email":"alice@example.org", "password":"password"}

        response = self.client.post(
            "/accounts/login/", payload, content="application/json")
        # check redirection to chceks
        self.assertRedirects(response, "/checks/")

    def test_login_with_bad_token(self):
        """ Login with a bad token and check that it redirects """

        # test using random token
        response = self.client.post(reverse("hc-check-token", args =["alice", "vhjf"]))

        # check redirection to login
        self.assertRedirects(response, "/accounts/login/")
