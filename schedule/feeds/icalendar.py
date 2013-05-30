import vobject

from django.conf import settings
from django.http import HttpResponse

EVENT_ITEMS = (
    ('uid', 'uid'),
    # ('dtstamp', 'dtstamp'),
    # ('contact', 'contact'),
    # ('description', 'description'),
    ('dtstart', 'start'),
    ('dtend', 'end'),
    ('location', 'location'),
    # ('rrule', 'rrule'),
    ('summary', 'summary'),
    # ('url', 'url'),
    # ('x-cost', 'x-cost'),
    # ('last_modified', 'last_modified'),
    # ('created', 'created'),
)

class ICalendarFeed(object):

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        cal = vobject.iCalendar()
        cal.calscale = 'GREGORIAN'
        cal.x_wr_timezone = settings.TIME_ZONE

        for item in self.items():

            event = cal.add('vevent')

            for vkey, key in EVENT_ITEMS:
                value = getattr(self, 'item_' + key)(item)
                if value:
                    event.add(vkey).value = value

        response = HttpResponse(cal.serialize())
        response['Content-Type'] = 'text/calendar'

        return response

    def items(self):
        return []

    def item_uid(self, item):
        pass

    def item_start(self, item):
        pass

    def item_end(self, item):
        pass

    def item_summary(self, item):
        return str(item)

    def item_location(self, item):
        pass

    def item_last_modified(self, item):
        pass

    def item_created(self, item):
        pass