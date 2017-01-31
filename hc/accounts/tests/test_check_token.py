from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
        self.client.login(username="alice", password="password")

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    # Login and test it redirects already logged in
    def test_login_and_redirects_already_logged_in(self):
        payload = {"email":"alice@example.org", "password":"password"}
        response = self.client.post("/accounts/login/", payload, content = "application/json")
        # chcek redirection to chceks
        self.assertRedirects(response, "/checks/")

    # Login with a bad token and check that it redirects
    def test_login_with_bad_token(self):
        payload = {"email":"alice@example.org", "password":"password"}
        # bad token
        self.profile.token = 'dcdf'
        response = self.client.post("/accounts/check_token/alice/rgrn/")
        # check redirection to login
        self.assertRedirects(response, "/accounts/login/")

    ### Any other tests?
