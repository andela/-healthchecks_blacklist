from hc.test import BaseTestCase
from hc.api.models import Check


class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        """ Test switching team."""
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url, follow=True)

        # Assert the contents of response
        # bob is in alices, redirectio to checks
        self.assertRedirects(response, "/checks/")


    def test_it_checks_team_membership(self):
        """ Test checking team membership."""
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url)
        # Assert the expected error code
        # error no access - access forbidden 403
        self.assertEqual(response.status_code, 403)

    def test_it_switches_to_own_team(self):
        """ Test switching to own team."""
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url, follow=True)
        ### Assert the expected error code
        self.assertRedirects(response, "/checks/")
        self.assertEqual(response.status_code, 200)
        
        
