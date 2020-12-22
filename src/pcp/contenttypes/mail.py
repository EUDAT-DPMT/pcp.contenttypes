import os
import six
import string
import pkg_resources
from email.utils import formataddr
from email.mime.text import MIMEText
from plone import api
from Products.CMFPlone.utils import safe_text

from zopyx.plone.persistentlogger.logger import PersistentLoggerAdapter


class Formatter(string.Formatter):
    def format(self, fmt, *args, **kw):
        field_names = [tp[1] for tp in self.parse(fmt)]
        for name in field_names:
            if name not in kw:
                kw[str(name)] = u''
            else:
                kw[str(name)] = safe_text(kw[str(name)])

        return super(Formatter, self).format(fmt, *args, **kw)


def send_mail(
    sender,
    recipients,
    subject,
    template,
    params,
    cc=None,
    cc_admin=False,
    context=None,
    admin_alternative_email=None,
):

    if 'NO_MAIL' in os.environ:
        return

    if not cc:
        cc = []

    footer_text = pkg_resources.resource_string(
        'pcp.contenttypes.templates', 'footer.txt'
    )
    params['footer'] = safe_text(footer_text)

    formatter = Formatter()
    email_text = pkg_resources.resource_string('pcp.contenttypes.templates', template)

    email_text = safe_text(email_text)
    email_text = formatter.format(email_text, **params)
    email_from_address = api.portal.get_registry_record('plone.email_from_address')
    email_from_name = api.portal.get_registry_record('plone.email_from_name')

    msg = MIMEText(email_text.encode('utf-8'), _charset='utf8')
    msg.set_charset('utf-8')
    recipients = [r for r in recipients if r]
    msg['To'] = ','.join(recipients)
    if sender:
        msg['From'] = sender
    else:
        portal = api.portal.get()
        msg['From'] = formataddr((email_from_name, email_from_address))
    if cc_admin:
        if admin_alternative_email:
            cc.append(admin_alternative_email)
        else:
            cc.append(email_from_address)
    if cc:
        msg['CC'] = ','.join(cc)
    msg['Subject'] = subject

    if context:
        PersistentLoggerAdapter(context).log(
            u'Mail "{}" to {}  + {}, Subject: "{}" sent'.format(
                subject, recipients, cc, subject
            )
        )

    mh = api.portal.get_tool('MailHost')
    mh.send(msg.as_string(), immediate=True)
