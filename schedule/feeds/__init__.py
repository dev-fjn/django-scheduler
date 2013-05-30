import datetime, itertools

from django.contrib.syndication.views import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone

from schedule.feeds.atom import Feed
from schedule.feeds.icalendar import ICalendarFeed
from schedule.models import Calendar


class UpcomingEventsFeed(Feed):
    feed_id = "upcoming"

    def feed_title(self, obj):
        return "Upcoming Events for %s" % obj.name

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Calendar.objects.get(pk=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        return itertools.islice(obj.occurrences_after(timezone.now()),
            getattr(settings, "FEED_LIST_LENGTH", 10))

    def item_id(self, item):
        return str(item.id)

    def item_title(self, item):
        return item.event.title

    def item_authors(self, item):
        if item.event.creator is None:
            return [{'name': ''}]
        return [{"name": item.event.creator.username}]

    def item_updated(self, item):
        return item.event.created_on

    def item_content(self, item):
        return "%s \n %s" % (item.event.title, item.event.description)


class CalendarICalendar(ICalendarFeed):
    def items(self):
        cal_id = self.args[1]
        cal = Calendar.objects.get(pk=cal_id)

        # return cal.events.all()
        return cal.occurrences_after()

    def item_uid(self, item):
        return item.get_absolute_url()

    def item_start(self, item):
        return item.start

    def item_end(self, item):
        return item.end

    def item_summary(self, item):
        return item.title

    def item_created(self, item):
        return item.event.created_on

    def item_description(self, item):
        return item.event.description

    def item_location(self, item):
        attr_list = ['venue_name', 'address']
        contact_details = [getattr(item.event, x) for x in attr_list if getattr(item.event, x) != '']
        return u'; '.join(contact_details)

    def item_url(self, item):
        # TODO: get full path including domain
        return item.get_absolute_url()

    def item_description(self, item):
        return item.description

    def item_contact(self, item):
        attr_list = ['contact', 'phone_number', 'email', 'url']
        contact_details = [getattr(item.event, x) for x in attr_list if getattr(item.event, x) != '']
        return u'; '.join(contact_details)

    def item_x_cost(self, item):
        return item.event.cost