from hc.api.models import Check, Channel
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    def setUp(self):
        super(AddCheckTestCase, self).setUp()

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        self.assertEqual(Check.objects.count(), 1)

    def test_team_access_works(self):
        """ Test that team access works."""
        url = "/checks/add/"

        # Logging in as bob, not alice. Bob has team access so this should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)
        check = Check.objects.get()
        self.assertEqual(check.user, self.alice)