from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    def test_team_access_works(self):
        test_channel = Channel(user=self.alice, kind="email")
        test_channel.save()
        alice_url = reverse("hc-channel-checks", args=[test_channel.code])
        #login Bob who is in alice's team
        self.client.login(username="bob@example.org", password="password")
        results = self.client.get(alice_url)
        self.assertEqual(results.status_code, 200)

    def test_bad_kind_not_working(self):
        ### Test that bad kinds don't work
        self.client.login(username="alice@example.org", password="password")
        kinds = ("bad kind 1", "bad kind 1")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
