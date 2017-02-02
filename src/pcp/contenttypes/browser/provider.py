

from datetime import datetime

import plone.api
from BTrees.OOBTree import OOBTree
from zope.interface import alsoProvides
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from plone.protect.interfaces import IDisableCSRFProtection

from ..mail import send_mail


NOTIFICATION_KEY = 'pcp.contenttypes.provider.notification'
RESEND_AFTER_DAYS = 7


class RegisteredServiceComponents(BrowserView):

    def items(self):
        """ Accumulatated view over all RegisteredServiceComponents """

        catalog = plone.api.portal.get_tool('portal_catalog')
        result = list()

        for brain in catalog(portal_type='Provider'):
            provider = brain.getObject()

            for brain2 in catalog(portal_type='RegisteredServiceComponent', path='/'.join(provider.getPhysicalPath())):
                rsc = brain2.getObject()
                version_info=rsc.check_versions()

            result.append(dict(
                provider=provider,
                component=rsc,
                version_info=version_info
                ))

        return result

    def notify_outdated(self):
        """ Notify providers by email about outdated implementations """

        # f*ck plone.protect
        alsoProvides(self.request, IDisableCSRFProtection)

        # remember when we send notifications for which component
        annotations = IAnnotations(self.context)
        notifications = annotations.get(NOTIFICATION_KEY)
        if not notifications:
            annotations[NOTIFICATION_KEY] = OOBTree()

        result = self.items()
        for item in self.items():

            version_info = item['version_info']

            # filter out irrelevant components
            if not version_info or version_info['is_current']:
                continue

            # preserve notification dates
            notification_key = (item['component'].getId(), version_info['current_version'], version_info['latest_version'])
            dt = annotations[NOTIFICATION_KEY].get(notification_key)
            if dt and (datetime.utcnow() - dt).days < RESEND_AFTER_DAYS:
                continue

            annotations[NOTIFICATION_KEY][notification_key] = datetime.utcnow()
            annotations._p_changed = True

            # build and send notification email
            dest_email = item['provider'].getAlarm_email() or item['provider'].getHelpdesk_email()
            subject = '[DPMT] New version for "{}" available'.format(item['component'].Title())

            params = dict(
                    component_name=item['component'].Title(),
                    component_url=item['component'].absolute_url(),
                    current_version=version_info['current_version'],
                    latest_version=version_info['latest_version'],
                    )
            send_mail(
                    sender=None,
                    recipients=[dest_email],
                    subject=subject,
                    template='implementation-outdated.txt',
                    params=params,
                    context=item['provider'])
        return 'DONE'
