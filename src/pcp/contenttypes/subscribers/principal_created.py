import plone
from pcp.contenttypes.mail import send_mail


def principal_created(event):
    try:
        portal = plone.api.portal.get()
    except plone.api.exc.CannotGetPortalError:
        return

    principal = event.principal
    user = plone.api.portal.get_tool('portal_membership').getMemberById(principal.getId())

    params = {
        'fullname': user.getProperty('fullname'),
        'email': user.getProperty('email'),
        'id': principal.getId()
    }

    send_mail(
        sender=None,
        recipients=[portal.email_from_address],
        subject='A new user visited DPMT',
        template='user-created-by-auto-user-maker.txt',
        params=params,
        context=None)
