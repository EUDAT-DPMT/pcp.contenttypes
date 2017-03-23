from ZODB.POSException import ConflictError

from zopyx.plone.persistentlogger.logger import IPersistentLogger


def create_accounting_account(obj, event):
    """ Create an IAccount for a registered resource during object creation """

    logger = IPersistentLogger(obj)

    try:
        obj.addAccount()
        logger.log('Account created on accounting server', level='info')
    except ConflictError:
        raise
    except Exception as e:
        pass
