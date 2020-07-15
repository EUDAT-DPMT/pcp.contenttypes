# -*- extra stuff goes here -*-
from pcp.contenttypes.interfaces.registeredstorageresource import IRegisteredStorageResource
from pcp.contenttypes.interfaces.registeredcomputeresource import IRegisteredComputeResource
from pcp.contenttypes.interfaces.serviceoffer import IServiceOffer
from pcp.contenttypes.interfaces.accountingrecord import IAccountingRecord
from pcp.contenttypes.interfaces.downtime import IDowntime
from pcp.contenttypes.interfaces.servicecomponentimplementationdetails import IServiceComponentImplementationDetails
from pcp.contenttypes.interfaces.servicecomponentimplementation import IServiceComponentImplementation
from pcp.contenttypes.interfaces.servicecomponent import IServiceComponent
from pcp.contenttypes.interfaces.servicedetails import IServiceDetails
from pcp.contenttypes.interfaces.registeredresource import IRegisteredResource
from pcp.contenttypes.interfaces.registeredservicecomponent import IRegisteredServiceComponent
from pcp.contenttypes.interfaces.registeredservice import IRegisteredService
from pcp.contenttypes.interfaces.resourcerequest import IResourceRequest
from pcp.contenttypes.interfaces.servicecomponentrequest import IServiceComponentRequest
from pcp.contenttypes.interfaces.servicerequest import IServiceRequest
from pcp.contenttypes.interfaces.servicecomponentoffer import IServiceComponentOffer
from pcp.contenttypes.interfaces.resourceoffer import IResourceOffer
from pcp.contenttypes.interfaces.plan import IPlan
from pcp.contenttypes.interfaces.environment import IEnvironment
from pcp.contenttypes.interfaces.provider import IProvider
from pcp.contenttypes.interfaces.person import IPerson
from pcp.contenttypes.interfaces.resource import IResource
from pcp.contenttypes.interfaces.center import ICenter
from pcp.contenttypes.interfaces.community import ICommunity
from pcp.contenttypes.interfaces.project import IProject
from pcp.contenttypes.interfaces.service import IService
from pcp.contenttypes.interfaces.accountable import IAccountable
from pcp.contenttypes.interfaces.rolerequest import IRoleRequest
from pcp.contenttypes.interfaces.actionitem import IActionItem
from pcp.contenttypes.interfaces.actionlist import IActionList
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPcpContenttypesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
