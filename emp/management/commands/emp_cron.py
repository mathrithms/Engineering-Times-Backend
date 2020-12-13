from django.core.management.base import BaseCommand
from django.utils import timezone
from emp.models import Job, Intern
import pytz


class Command(BaseCommand):
    help = "cron jobs for emp module"

    def handle(self, *args, **kwargs):
        tz = 'Asia/Kolkata'
        timezone.activate(pytz.timezone(tz))
        Job.objects.filter(expire__lt=timezone.now()).delete()
        Intern.objects.filter(expire__lt=timezone.now()).delete()
        self.stdout.write("Deleted unneccessary objects")
