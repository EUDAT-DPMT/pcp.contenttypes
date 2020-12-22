from collective import dexteritytextindexer
from collective.relationhelpers import api as relapi
from pcp.contenttypes.content_dx.provider import IProvider
from pcp.contenttypes.content_dx.registeredservice import IRegisteredService
from pcp.contenttypes.content_dx.registeredservicecomponent import \
    IRegisteredServiceComponent
from pcp.contenttypes.mail import send_mail
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer

import datetime
import pytz


class IDowntime(model.Schema):
    """Dexterity Schema for Downtimes"""

    dexteritytextindexer.searchable('start', 'end', 'severity', 'classification')

    start = schema.Datetime(
        title='Start date (UTC)',
        description='When does the downtime start? In UTC!',
        required=True,
    )
    directives.widget(
        'start',
        DatetimeFieldWidget,
        default_timezone='UTC',
    )

    end = schema.Datetime(
        title='End date (UTC)',
        description='When does the downtime end? In UTC!',
        required=True,
    )
    directives.widget(
        'end',
        DatetimeFieldWidget,
        default_timezone='UTC',
    )

    affected_registered_services = RelationList(
        title='Affected registered services',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'affected_registered_services',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': [
                'registeredservice_dx',
                'registeredservicecomponent_dx',
            ],
            'basePath': make_relation_root_path,
        },
    )

    reason = schema.URI(
        title='Reason',
        description='Optional URL to the change management document providing the reason for this downtime.',
        required=False,
    )

    severity = schema.Choice(
        title='Severity',
        vocabulary='dpmt.severity_levels',
        required=False,
    )

    classification = schema.Choice(
        title='Classification',
        vocabulary='dpmt.downtime_classes',
        required=False,
    )


@implementer(IDowntime)
class Downtime(Container):
    """Downtime instance"""

    # for the GOCDB compatibility layer
    def naive_start(self):
        """'start' without explicit time zone"""
        return self.start.strftime('%Y-%m-%d %H:%M')

    def naive_end(self):
        """'end' without explicit time zone"""
        return self.end.strftime('%Y-%m-%d %H:%M')

    # BBB
    @property
    def startDateTime(self):
        return self.start

    @property
    def endDateTime(self):
        return self.end


def findDowntimeRecipients(downtime):
    affected_services_or_components = relapi.unrestricted_relations(
        downtime, 'affected_registered_services'
    )

    affected_components = [
        component
        for component in affected_services_or_components
        if IRegisteredServiceComponent.providedBy(component)
    ]

    indirectly_affected_services = []
    for component in affected_components:
        indirectly_affected_services += relapi.unrestricted_backrelations(
            component, 'service_components'
        )

    indirectly_affected_services = set(indirectly_affected_services)

    directly_affected_services = {
            service
            for service in affected_services_or_components
            if IRegisteredService.providedBy(service)
    }

    affected_services = set.union(
        directly_affected_services, indirectly_affected_services
    )

    affected_projects = []
    for affected_service in affected_services:
        affected_projects += relapi.unrestricted_backrelations(
            affected_service, 'registered_services_used'
        )

    affected_communities = [
        relapi.relation(project, 'community') for project in affected_projects
    ]

    project_contacts = [
        relapi.relation(project, 'community_contact', restricted=False)
        for project in affected_projects
    ]
    project_contacts_emails = {i.email for i in project_contacts if i.email}

    community_admins = []
    for community in affected_communities:
        community_admins.extend(relapi.relations(community, 'community_admins'))
    community_admin_emails = {i.email for i in community_admins if i.email}

    recipients = set.union(project_contacts_emails, community_admin_emails)
    return recipients


def _getCurrentTime():
    return datetime.datetime.now(pytz.timezone('UTC'))


def notifyDowntimeRecipients(downtime, subject, template, recipients):
    if downtime.end + datetime.timedelta(hours=1) < _getCurrentTime():
        # do not send notifications for past downtimes
        return

    affected_services = [i.to_object for i in downtime.affected_registered_services]

    chain = downtime.aq_chain
    provider = None
    for element in chain:
        if IProvider.providedBy(element):
            provider = element
            break
    assert provider

    params = {
        'description': downtime.description,
        # UTC because we have no clue in which timezone the recipient is (using Plone 4)
        'start_date': str(downtime.start),
        'end_date': str(downtime.end),
        'provider_name': provider.title,
        'provider_url': provider.url,
        'contact_mail_alarm': provider.alarm_email,
        'contact_mail_helpdesk': provider.helpdesk_email,
        'contact_phone_emergency': provider.emergency_phone,
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
            context=downtime,
        )


def sendDowntimeMails(downtime, subject, template):
    recipients = findDowntimeRecipients(downtime)
    notifyDowntimeRecipients(downtime, subject, template, recipients)


def announceDowntime(downtime):
    sendDowntimeMails(downtime, '[DPMT] Upcoming Downtime', 'announce-downtime.txt')


def retractDowntime(downtime):
    sendDowntimeMails(downtime, '[DPMT] Retracted Downtime', 'retract-downtime.txt')


def handleDowntimeTransition(context, event):
    assert (
        event.workflow.id == 'downtime_workflow'
    ), 'expecting Downtime Workflow being assigned to Downtime'

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
