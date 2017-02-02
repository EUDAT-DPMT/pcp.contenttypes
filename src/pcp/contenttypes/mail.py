

import os
import string
import pkg_resources
from email.utils import formataddr
from email.MIMEText import MIMEText

import plone.api
from zopyx.plone.persistentlogger.logger import PersistentLoggerAdapter


class Formatter(string.Formatter):

    def format(self, fmt, *args, **kw):
        field_names = [tp[1] for tp in self.parse(fmt)]
        for name in field_names:
            if not name in kw:
                kw[str(name)] = u''
            else:
                if not isinstance(kw[str(name)], unicode):
                    kw[str(name)] = unicode(kw[str(name)], 'utf8')

        return super(Formatter, self).format(fmt, *args, **kw)


def send_mail(sender, recipients, subject, template, params, cc=None, cc_admin=False, context=None, admin_alternative_email=None):

    if 'NO_MAIL' in os.environ:
        return

    if not cc:
        cc = []

    footer_text = pkg_resources.resource_string(
        'pcp.contenttypes.templates', 'footer.txt')
    params['footer'] = unicode(footer_text, 'utf-8')

    formatter = Formatter()
    email_text = pkg_resources.resource_string(
        'pcp.contenttypes.templates', template)

    try:
        email_text = unicode(email_text, 'utf-8')
    except UnicodeError:
        email_text = unicode(email_text, 'iso-8859-15')

    email_text = formatter.format(email_text, **params)

    msg = MIMEText(email_text.encode('utf-8'), _charset='utf8')
    msg.set_charset('utf-8')
    recipients = [r for r in recipients if r]
    msg['To'] = ','.join(recipients)
    if sender:
        msg['From'] = sender
    else:
        portal = plone.api.portal.get()
        msg['From'] = formataddr(
            (portal.email_from_name, portal.email_from_address))
    if cc_admin:
        if admin_alternative_email:
            cc.append(admin_alternative_email)
        else:
            cc.append(portal.email_from_address)
    if cc:
        msg['CC'] = ','.join(cc)
    msg['Subject'] = subject

    if context:
        PersistentLoggerAdapter(context).log(
            u'Mail "{}" to {}  + {}, Subject: "{}" sent'.format(subject, recipients, cc, subject))

    mh = plone.api.portal.get_tool('MailHost')
    mh.send(msg.as_string(), immediate=True)
