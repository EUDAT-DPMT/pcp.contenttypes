"""Definition of the Downtime content type
"""

from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.mail import send_mail
from zope.interface import implements

from Products.Archetypes.Widget import CalendarWidget, ComputedWidget

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IDowntime
from pcp.contenttypes.config import PROJECTNAME

from DateTime import DateTime


class DateComputedField(atapi.ComputedField):

    def get(self, instance, **kwargs):
        """Return the computed value."""
        instance = eval(self.expression, {'context': instance, 'here': instance})
        # Plone DateTime does not show timezone via %Z
        return instance.asdatetime().strftime("%Y-%m-%d %H:%M %Z")


DowntimeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.DateTimeField('startDateTime',
                        required=True,
                        searchable=False,
                        accessor='start',  # compare ATContentTypes - Event
                        default_method=DateTime,
                        languageIndependent=True,
                        hidden=True,
                        widget=CalendarWidget(label='Start date (CET)',
                                              description='When does the downtime start? In CET!'),
                        ),

    DateComputedField('startDateTimeUtc',
                      expression="here.start().toZone('UTC')",
                      widget=ComputedWidget(label='Start date (UTC)'),
                      ),

    DateComputedField('startDateTimeCet',
                      expression="here.start().toZone('CET')",
                      widget=ComputedWidget(label='Start date (CET)'),
                      ),

    atapi.DateTimeField('endDateTime',
                        required=True,
                        searchable=False,
                        accessor='end',  # compare ATContentTypes - Event
                        default_method=DateTime,
                        languageIndependent=True,
                        hidden=True,
                        widget=CalendarWidget(label='End date (CET)',
                                              description='When does the downtime end? In CET!'),
                        ),

    DateComputedField('endDateTimeUtc',
                      expression="here.end().toZone('UTC')",
                      widget=ComputedWidget(label='End date (UTC)'),
                      ),

    DateComputedField('endDateTimeCet',
                      expression="here.end().toZone('CET')",
                      widget=ComputedWidget(label='End date (CET)'),
                      ),

    atapi.ReferenceField('affected_registered_serivces',
                         relationship='affected_registered_services',
                         allowed_types=('RegisteredService', 'RegisteredServiceComponent',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Affected registered services',
                                                       description='All registered services and components unavailable during downtime',
                                                       allow_browse=1,
                                                       startup_directory='/pcp/'
                                                       ),
                         ),

))


schemata.finalizeATCTSchema(DowntimeSchema, moveDiscussion=False)


class Downtime(base.ATCTContent):
    """Scheduled downtime"""
    implements(IDowntime)

    meta_type = "Downtime"
    schema = DowntimeSchema


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


def notifyDowntimeRecipients(downtime, subject, template, recipients):
    affected_services = downtime.getAffected_registered_serivces()

    provider_brains = downtime.portal_catalog(portal_type='Provider', path='/'.join(downtime.getPhysicalPath()[0:4]))

    assert len(provider_brains) == 1
    for brain in provider_brains:
        provider = brain.getObject()

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
