
import inspect
from zopyx.plone.persistentlogger.logger import IPersistentLogger

def SharingHandler(event):
    """ Log/intercept @@sharing changes """

    context = event.object
    logger = IPersistentLogger(context)
    print event.diff_context
    logger.log('Sharing updated',
            level='info',
            details=event.diff_context)

