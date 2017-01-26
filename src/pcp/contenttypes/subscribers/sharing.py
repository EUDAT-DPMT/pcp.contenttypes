
import plone.api
from zopyx.plone.persistentlogger.logger import IPersistentLogger

def SharingHandler(event):
    """ Log/intercept @@sharing changes """

    context = event.object
    logger = IPersistentLogger(context)

    user = plone.api.user.get_current()
    username = user.getUserName()
    email = user.getProperty('email')
    fullname = user.getProperty('fullname')
    username = '{} ({}, {})'.format(username, fullname, email)
    info_url = 'http://www.heise.de'

    logger.log('Sharing updated',
            level='info',
            username=username,
            info_url=info_url,
            details=event.diff_context)

