from django.core.management.base import NoArgsCommand
from event.models import Event
from django.utils import timezone
import pytz
# import datetime


class Command(NoArgsCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **kwargs):
        # date_today = datetime.date.today()
        tz = 'Asia/Kolkata'
        timezone.activate(pytz.timezone(tz))
        Event.objects.filter(time__lt=timezone.now()).delete()
