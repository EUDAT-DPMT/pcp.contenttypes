"""Definition of the Downtime content type
"""
import datetime

from pcp.contenttypes.interfaces import IProvider
from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.mail import send_mail
from plone.formwidget.datetime.at import DatetimeWidget
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary

# -*- Message Factory Imported Here -*-

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IDowntime
from pcp.contenttypes.config import PROJECTNAME

from DateTime import DateTime


DowntimeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.DateTimeField('startDateTime',
                        required=True,
                        searchable=True,
                        accessor='start',  # compare ATContentTypes - Event
                        default_method=DateTime,
                        languageIndependent=True,
                        widget=DatetimeWidget(label='Start date (UTC)',
                                              pattern='yyyy/MM/dd HH:mm:ss UTC',
                                              description='When does the downtime start? In UTC!'),
                        ),

    atapi.DateTimeField('endDateTime',
                        required=True,
                        searchable=True,
                        accessor='end',  # compare ATContentTypes - Event
                        default_method=DateTime,
                        languageIndependent=True,
                        widget=DatetimeWidget(label='End date (UTC)',
                                              pattern='yyyy/MM/dd HH:mm:ss UTC',
                                              description='When does the downtime end? In UTC!'),
                        ),

    atapi.ReferenceField('affected_registered_serivces',
                         relationship='affected_registered_services',
                         allowed_types=('RegisteredService', 'RegisteredServiceComponent',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Affected registered services',
                                                       description='All registered services and components unavailable during downtime',
                                                       allow_browse=1,
                                                       startup_directory_method='getStartupDirectory',
                                                       ),
                         ),
    ateapi.UrlField('reason',
                    widget=ateapi.UrlWidget(label='Reason',
                                            description='Optional URL to the change management document providing the reason for this downtime.',
                                        ),
                ),
    atapi.StringField('severity',
                      searchable=1,
                      default='warning',
                      vocabulary=NamedVocabulary('severity_levels'),
                      widget=atapi.SelectionWidget(label='Severity',
                                                   ),
                      ),
    atapi.StringField('classification',
                      searchable=1,
                      default='scheduled',
                      vocabulary=NamedVocabulary('downtime_classes'),
                      widget=atapi.SelectionWidget(label='Classification',
                                                   ),
                      ),
))

schemata.finalizeATCTSchema(DowntimeSchema, moveDiscussion=False)


class Downtime(base.ATCTContent):
    """Scheduled downtime"""
    implements(IDowntime)

    meta_type = "Downtime"
    schema = DowntimeSchema

    def _setDateTimeField(self, fieldName, value):
        if not isinstance(value, DateTime):
            value = DateTime(value)

        if value.timezoneNaive():
            parts = value.parts()
            value = DateTime(*(parts[:-1] + ('UTC',)))
        else:
            value = value.toZone('UTC')

        self.Schema()[fieldName].set(self, value)

    def setStartDateTime(self, value):
        self._setDateTimeField('startDateTime', value)

    def setEndDateTime(self, value):
        self._setDateTimeField('endDateTime', value)

    def getStartupDirectory(self):
        parent = self.aq_parent
        if IProvider.providedBy(parent):
            return '/'.join(parent.getPhysicalPath())
        else:
            return self.portal_url.getPortalPath()

    # for the GOCDB compatibility layer
    def naive_start(self):
        """'start' without explicit time zone"""
        return self.start().strftime("%Y-%m-%d %H:%M")

    def naive_end(self):
        """'end' without explicit time zone"""
        return self.end().strftime("%Y-%m-%d %H:%M")



atapi.registerType(Downtime, PROJECTNAME)


def findDowntimeRecipients(downtime):
    # TODO: Maybe avoid 'dereferencing' objects by using relation objects manually instead via backreferences
    affected_services_or_components = downtime.getAffected_registered_serivces()

    affected_components = [component for component in affected_services_or_components
                           if IRegisteredServiceComponent.providedBy(component)]

    indirectly_affected_services = set([service for component in affected_components
                                        for service in component.getParent_services()])

    directly_affected_services = set([service for service in affected_services_or_components
                                      if IRegisteredService.providedBy(service)])

    affected_services = set.union(directly_affected_services, indirectly_affected_services)
    affected_projects = [project for service in affected_services
                         for project in service.getUsed_by_projects()]
    affected_communities = [project.getCommunity() for project in affected_projects if project.getCommunity()]

    project_contacts = set([project.getCommunity_contact().getEmail()
                            for project in affected_projects
                            if project.getCommunity_contact() and project.getCommunity_contact().getEmail()])
    community_admins = set([admin.getEmail()
                            for community in affected_communities
                            for admin in community.getAdmins()
                            if admin.getEmail()])

    recipients = set.union(project_contacts, community_admins)
    return recipients


def _getCurrentTime():
    now = datetime.datetime.utcnow()
    return DateTime(now)


def notifyDowntimeRecipients(downtime, subject, template, recipients):
    if downtime.end() + 1 < _getCurrentTime():
        # do not send notifications for past downtimes
        return

    affected_services = downtime.getAffected_registered_serivces()

    chain = downtime.aq_chain
    provider = None
    for element in chain:
        if IProvider.providedBy(element):
            provider = element
            break
    assert provider

    params = {
        'description': downtime.Description(),
        # UTC because we have no clue in which timezone the recipient is (using Plone 4)
        'start_date': str(downtime.start().toZone('UTC')),
        'end_date': str(downtime.end().toZone('UTC')),
        'provider_name': provider.title,
        'provider_url': provider.url,
        'contact_mail_alarm': provider.getAlarm_email(),
        'contact_mail_helpdesk': provider.getHelpdesk_email(),
        'contact_phone_emergency': provider.getEmergency_phone(),
        'services': '\n'.join(['* ' + service.title for service in affected_services]),
        'downtime_link': downtime.absolute_url(),
    }

    for recipient in recipients:
        send_mail(
                sender=None,
                recipients=[recipient],
                subject=subject,
                template=template,
                params=params,
                context=downtime)


def sendDowntimeMails(downtime, subject, template):
    recipients = findDowntimeRecipients(downtime)
    notifyDowntimeRecipients(downtime, subject, template, recipients)


def announceDowntime(downtime):
    sendDowntimeMails(downtime, '[DPMT] Upcoming Downtime', 'announce-downtime.txt')


def retractDowntime(downtime):
    sendDowntimeMails(downtime, '[DPMT] Retracted Downtime', 'retract-downtime.txt')


def handleDowntimeTransition(context, event):
    assert event.workflow.id == 'downtime_workflow', \
        'expecting Downtime Workflow being assigned to Downtime'

    new_state = getattr(event.new_state, 'id', None)
    old_state = getattr(event.old_state, 'id', None)
    transition = getattr(event.transition, 'id', None)

    downtime = event.object

    if new_state == 'published' and transition == 'publish':
        assert old_state != 'published'
        announceDowntime(downtime)

    if old_state == 'published' and transition in ('reject', 'retract'):
        assert new_state != 'published'
        retractDowntime(downtime)
