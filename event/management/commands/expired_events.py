from django.core.management.base import NoArgsCommand
from event.models import Event
import datetime


class Command(NoArgsCommand):

    help = 'Expires event objects which are out-of-date'

    def handle_noargs(self):
        date_today = datetime.date.today()
        Event.objects.filter(time__lt=date_today).delete()
