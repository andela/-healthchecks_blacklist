from datetime import timedelta
import time

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from hc.accounts.models import Profile
from hc.api.models import Check


def num_pinged_checks(profile):
    q = Check.objects.filter(user_id=profile.user.id,)
    q = q.filter(last_ping__isnull=False)
    return q.count()


class Command(BaseCommand):
    help = 'Send due monthly reports'
    tmpl = "Sending monthly report to %s"

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            dest='loop',
            default=False,
            help='Keep running indefinitely in a 300 second wait loop',
        )

    def handle_one_run(self):
        now = timezone.now()
        day_before = now - timedelta(minutes=1)
        week_before = now - timedelta(days=7)
        month_before = now - timedelta(days=30)

        report_due = Q(next_report_date__lt=now)
        report_not_scheduled = Q(next_report_date__isnull=True)
        sent = 0

        import pdb; pdb.set_trace()

        q1 = Profile.objects.filter(report_due | report_not_scheduled)
        q2 = q1.filter(daily_reports_allowed=True)
        q3 = q2.filter(user__date_joined__lt=day_before)
        for profile in q3:
            if num_pinged_checks(profile) > 0:
                self.stdout.write(self.tmpl % profile.user.email)
                profile.send_report()
                sent += 1

        q = Profile.objects.filter(report_due | report_not_scheduled)
        q = q.filter(weekly_reports_allowed=True)
        q = q.filter(user__date_joined__lt=week_before)
        for profile in q:
            if num_pinged_checks(profile) > 0:
                self.stdout.write(self.tmpl % profile.user.email)
                profile.send_report()
                sent += 1

        q = Profile.objects.filter(report_due | report_not_scheduled)
        q = q.filter(monthly_reports_allowed=True)
        q = q.filter(user__date_joined__lt=month_before)
        for profile in q:
            if num_pinged_checks(profile) > 0:
                self.stdout.write(self.tmpl % profile.user.email)
                profile.send_report()
                sent += 1

        return q1

    def handle(self, *args, **options):
        if not options["loop"]:
            return "Sent %s reports" % self.handle_one_run()

        self.stdout.write("sendreports is now running")
        while True:
            self.handle_one_run()

            formatted = timezone.now().isoformat()
            self.stdout.write("-- MARK %s --" % formatted)

            time.sleep(300)
