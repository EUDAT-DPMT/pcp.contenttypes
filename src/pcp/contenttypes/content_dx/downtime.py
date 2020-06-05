# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
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


class IDowntime(model.Schema):
    """Dexterity Schema for Downtimes
    """

    dexteritytextindexer.searchable(
        "start", "end", "severity", "classification"
    )

    start = schema.Datetime(
        title=u"Start date (UTC)",
        description=u"When does the downtime start? In UTC!",
        required=True,
    )
    directives.widget('start', DatetimeFieldWidget)

    end = schema.Datetime(
        title=u"End date (UTC)",
        description=u"When does the downtime end? In UTC!",
        required=True,
    )
    directives.widget('end', DatetimeFieldWidget)

    affected_registered_services = RelationList(
        title=u"Affected registered services",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "affected_registered_services",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["registeredservice_dx","registeredservicecomponent_dx"],
            "basePath": make_relation_root_path,
        },
    )

    reason = schema.URI(
        title=u"Reason",
        description=u"Optional URL to the change management document providing the reason for this downtime.",
        required=False,
    )

    severity = schema.Choice(
        title=u'Severity',
        vocabulary='dpmt.severity_levels',
        required=False,
        )

    classification = schema.Choice(
        title=u'Classification',
        vocabulary='dpmt.downtime_classes',
        required=False,
        )


@implementer(IDowntime)
class Downtime(Container):
    """Downtime instance"""

    # for the GOCDB compatibility layer
    def naive_start(self):
        """'start' without explicit time zone"""
        return self.start.strftime("%Y-%m-%d %H:%M")

    def naive_end(self):
        """'end' without explicit time zone"""
        return self.end.strftime("%Y-%m-%d %H:%M")


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
