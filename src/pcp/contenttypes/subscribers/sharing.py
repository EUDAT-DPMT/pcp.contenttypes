
import inspect
from zopyx.plone.persistentlogger.logger import IPersistentLogger

def SharingHandler(event):
    """ Log/intercept @@sharing changes """

    context = event.object
    logger = IPersistentLogger(context)

    # *very evil* search the call stack for local variable 'settings' and 'inherit' in order
    # to find the caller issuing the notify() call.
    # plone.app.workflow-2.1.9-py2.7.egg/plone/app/workflow/browser/sharing.py

    for frame in inspect.stack():
        if 'settings' in frame[0].f_locals:
            settings = frame[0].f_locals['settings']
            inherit = frame[0].f_locals['inherit']
            logger.log('Sharing updated',
                    level='info',
                    details=dict(inherit=inherit, settings=settings))
            continue
