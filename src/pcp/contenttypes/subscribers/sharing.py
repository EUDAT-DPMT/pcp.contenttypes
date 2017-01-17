

from zopyx.plone.persistentlogger.logger import IPersistentLogger

def SharingHandler(event):
    context = event.object
    request = event.descriptions[0]
    form = request.form

    logger = IPersistentLogger(context)
    print context
    logger.log('Sharing updated',
            level='info',
            details=dict(request.form))
