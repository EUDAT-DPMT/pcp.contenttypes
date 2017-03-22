"""Definition of the RoleRequest content type
"""
import plone
from Products.Archetypes.Widget import TextAreaWidget, SelectionWidget
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from pcp.contenttypes.mail import send_mail
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces.rolerequest import IRoleRequest
from pcp.contenttypes.config import PROJECTNAME

RoleRequestSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField('userid',
                      relationship='rolerequest_for_userid',
                      allowed_types=(),
                      enforceVocabulary=True,
                      default_method='getSelectableUsersDefault',
                      required=True,
                      vocabulary='getSelectableUsers',
                      widget=SelectionWidget(label='User',
                                             format='select',
                                             description='Whom to grant the role to?',),
                      ),
    atapi.StringField('role',
                      enforceVocabulary=True,
                      vocabulary='getSelectableRoles',
                      required=True,
                      default='',
                      widget=SelectionWidget(label='Role',
                                             format='select',
                                             description='The role to be granted',),
                      ),
    atapi.ReferenceField('context',
                         relationship='rolerequest_for_context',
                         allowed_types=(),
                         vocabulary_display_path_bound=0,
                         required=True,
                         widget=ReferenceBrowserWidget(label='Context',
                                                       description='The context to grant the role for',
                                                       startup_directory='/',),
                         ),
    atapi.TextField('motivation',
                    required=True,
                    widget=TextAreaWidget(label='Motivation',
                                          description='Motivation of this request',
                                          allow_browse=True),
                    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

RoleRequestSchema['title'].storage = atapi.AnnotationStorage()
RoleRequestSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RoleRequestSchema, moveDiscussion=False)


class RoleRequest(base.ATCTContent):
    """Description of the Example Type"""
    implements(IRoleRequest)

    meta_type = "RoleRequest"
    schema = RoleRequestSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def getSelectableUsers(self):
        return [(str(user.getId()), "%s (%s)" % (user.getProperty('fullname'), user.getProperty('email')))
                for user in plone.api.user.get_users()]

    def getSelectableUsersDefault(self):
        current_user = plone.api.user.get_current()
        print current_user.getId()
        return str(current_user.getId())

    def getSelectableRoles(self):
        disfavoured_roles = {'Anonymous', 'Authenticated', 'Contributor', 'Editor',
                             'Manager', 'Member', 'Reader', 'Site Administrator'}

        all_roles = set(self.valid_roles())
        return ['Select...'] + list(all_roles - disfavoured_roles)

    def validate_role(self, value):
        return 'Select a role!' if value == 'Select...' else None

atapi.registerType(RoleRequest, PROJECTNAME)



def logRoleGrant(context, receiver, role):
    # adapted from subscribers.sharing.SharingHandler
    # this function should be replaced by a factored out variant from patches.py:sharing_handle_form
    # to have an actual context-diff.

    from zopyx.plone.persistentlogger.logger import IPersistentLogger

    logger = IPersistentLogger(context)

    user = plone.api.user.get_current()
    username = user.getUserName()
    info_url = '/@@user-information?userid={}'.format(username)
    email = user.getProperty('email')
    fullname = user.getProperty('fullname')
    if fullname and email:
        username = '{} ({}, {})'.format(username, fullname, email)

    diff_context = {
        'role_changes': {
            receiver.getId(): {
                'fullname': receiver.getProperty('fullname'),
                'email': receiver.getProperty('email'),
                'added': {role,},
                'removed': set(),
            }
        }
    }

    logger.log('Sharing updated (via Role Request)',
               level='info',
               username=username,
               info_url=info_url,
               details=diff_context)


def handleRoleRequestTransition(context, event):
    assert event.workflow.id == 'rolerequest_workflow', \
        'expecting Rolerequest Workflow being assigned to RoleRequest'

    transition = getattr(event.transition, 'id', None)
    if transition not in ('accept', 'reject'):
        return

    request = context
    requester = context.getOwner()

    receiver = plone.api.user.get(userid=request.getUserid())
    role = request.getRole()
    request_context = request.getContext()

    plone.api.user.grant_roles(user=receiver,
                               obj=request_context,
                               roles=[role])

    logRoleGrant(request_context, receiver, role)

    params = {
        'role': role,
        'action': transition,
        'context_url': request_context.absolute_url(),
        'rolerequest_link': request.absolute_url(),
        'receiver_name': receiver.getProperty('fullname') or '[noname]',
        'receiver_email': receiver.getProperty('email') or '[nomail]',
        'requester_name': requester.getProperty('fullname') or '[noname]',
        'requester_email': requester.getProperty('email') or '[nomail]',
    }

    send_mail(
        sender=None,
        recipients={receiver.getProperty('email'), requester.getProperty('email')},
        subject='[DPMT] Accepted Role Request',
        template='role-request.txt',
        params=params,
        context=request)
