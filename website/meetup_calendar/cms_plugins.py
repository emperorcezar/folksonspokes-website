from calendar import HTMLCalendar
from collections import defaultdict

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from meetup import meetup_api_client as client


class MeetupHTMLCalendar(HTMLCalendar):
    def __init__(self, events, *args, **kwargs):
        super(MeetupHTMLCalendar, self).__init__(*args, **kwargs)
        self.events = events
        self.event_dict = defaultdict(list)
        
        for event in self.events:
            day = event.get_time().day
            self.event_dict[day].append(event)
        
    def formatday(self, day, weekday):
        """
          Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            td = '<td class="%s">%d' % (self.cssclasses[weekday], day)
            for event in self.event_dict[day]:
                td += '<br>' + event.name
            td += '</td>'

            return td
    
class MeetupCalendarPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Meetup Calendar")
    render_template = "meetup_calendar.html"

    def render(self, context, instance, placeholder):
        meetup = client.Meetup(settings.MEETUP_API_KEY)
        events = meetup.get_events(group_urlname = settings.MEETUP_GROUP_URLNAME)
        context.update({
            'events': events.results,
            'calendar': MeetupHTMLCalendar(events = events.results).formatmonth(2012, 10)
        })
        return context

plugin_pool.register_plugin(MeetupCalendarPlugin)