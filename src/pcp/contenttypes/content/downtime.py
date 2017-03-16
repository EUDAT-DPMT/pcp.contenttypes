"""Definition of the Downtime content type
"""
import Products
from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.mail import send_mail
from zope.interface import implements

from Products.Archetypes.Widget import CalendarWidget

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IDowntime
from pcp.contenttypes.config import PROJECTNAME

from DateTime import DateTime

from datetime import datetime
from pytz import utc as UTC

DowntimeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.DateTimeField('startDateTime',
                        required=True,
                        searchable=False,
                        accessor='start',  # compare ATContentTypes - Event
                        default_method=DateTime,
                        languageIndependent=True,
                        widget=CalendarWidget(label='Start date',
                                              description='When does the downtime start? In your local time!'),
                        ),

    atapi.DateTimeField('endDateTime',
                        required=True,
                        searchable=False,
                        accessor='end',  # compare ATContentTypes - Event
                        default_method=DateTime,
                        languageIndependent=True,
                        widget=CalendarWidget(label='End date',
                                              description='When does the downtime end? In your local time!'),
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
    affected_communities = [project.getCommunity() for project in affected_projects]

    project_contacts = set([project.getCommunity_contact().getEmail() for project in affected_projects])
    community_admins = set([admin.getEmail() for community in affected_communities for admin in community.getAdmins()])

    recipients = set.union(project_contacts, community_admins)
    return recipients


def notifyDowntimeRecipients(downtime, subject, template, recipients):
    affected_services = downtime.getAffected_registered_serivces()

    provider_brains = downtime.portal_catalog(portal_type='Provider', path='/'.join(downtime.getPhysicalPath()[0:4]))

    assert len(provider_brains) == 1
    for brain in provider_brains:
        provider = brain.getObject()

    for recipient in recipients:
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
        'expecting Simple Publication Workflow being assigned to Downtime'

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
