from collective.relationhelpers import api as relapi
from plone import api
from plone.app.contenttypes.migration.field_migrators import datetime_fixer
from plone.app.contenttypes.migration.migration import migrateCustomAT
from plone.event.utils import default_timezone
from Products.CMFPlone.utils import safe_text

import logging


log = logging.getLogger(__name__)

# Field Migrators


def migrate_adress(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate ateapi.AddressField to multiple dx fields"""
    address = src_obj.address
    dst_obj.street1 = safe_text(address.get('street1'))
    dst_obj.street2 = safe_text(address.get('street2'))
    dst_obj.zip = safe_text(address.get('zip'))
    dst_obj.city = safe_text(address.get('city'))
    dst_obj.country = safe_text(address.get('country'))


def migrate_simple_datagrid(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate RecordsField to datagrid if fieldnames are exactly the same;
    and simple (textline, list, tuple etc.)
    """
    at_values = src_obj.getField(src_fieldname).get(src_obj)
    dx_values = []
    for at_value in at_values:
        dx_value = {}
        for key, val in at_value.items():
            if isinstance(at_value, tuple):
                val = tuple(safe_text(i) for i in val)
            if isinstance(at_value, list):
                val = [safe_text(i) for i in val]
            dx_value[key] = val
        dx_values.append(dx_value)
    setattr(dst_obj, dst_fieldname, dx_values)


def migrate_vocabulary(src_obj, dst_obj, src_fieldname, dst_fieldname):
    # Migrate from ATVocabularymanager to manual Vocabularies built with
    # safe_simplevocabulary_from_values from registry values.
    # In AT the value is usually all-lowercase while in dx it is same as the title.
    # E.g. AT: "scheduled", DX: "Scheduled"
    from plone.dexterity.interfaces import IDexterityFTI
    from zope.component import getUtility
    from zope.schema.interfaces import IVocabularyFactory

    field = src_obj.getField(src_fieldname)
    at_value = field.get(src_obj)
    if not at_value:
        # empty value
        setattr(dst_obj, dst_fieldname, at_value)
        return

    voc = field.vocabulary
    fti = getUtility(IDexterityFTI, name=dst_obj.portal_type)
    dx_field, dx_schema = relapi.get_field_and_schema_for_fieldname(dst_fieldname, fti)
    if isinstance(at_value, (list, tuple)):
        dx_voc = getUtility(IVocabularyFactory, dx_field.value_type.vocabularyName)
        dx_voc = dx_voc(None)

        # deal with multiple choice fields
        dx_value = []
        for one_at_value in at_value:
            one_at_title = voc.getVocabularyDict(src_obj)[one_at_value]
            for term in dx_voc:
                if term.title == one_at_title:
                    dx_value.append(safe_text(term.value))
                    break
        setattr(dst_obj, dst_fieldname, dx_value)

    else:
        dx_voc = getUtility(IVocabularyFactory, dx_field.vocabularyName)
        dx_voc = dx_voc(None)
        at_title = voc.getVocabularyDict(src_obj)[at_value]
        for term in dx_voc:
            if term.title == at_title:
                dx_value = term.value
                break
        setattr(dst_obj, dst_fieldname, safe_text(dx_value))


def migrate_datetimefield(src_obj, dst_obj, src_fieldname, dst_fieldname):
    old_value = src_obj.getField(src_fieldname).get(src_obj)
    if not old_value:
        return
    if src_obj.getField('timezone', None) is not None:
        old_timezone = src_obj.getField('timezone').get(src_obj)
    else:
        old_timezone = default_timezone(fallback='UTC')
    new_value = datetime_fixer(old_value.asdatetime(), old_timezone)
    setattr(dst_obj, dst_fieldname, new_value)


# Field mappings for behaviors to inject into content-type mappings
# CommonFields => IDPMTCommon
fields_mapping_common = [
    {
        'AT_field_name': 'identifiers',
        'DX_field_name': 'identifiers',
        'field_migrator': migrate_simple_datagrid,
    },
    {
        'AT_field_name': 'additional',
        'DX_field_name': 'additional',
        'field_migrator': migrate_simple_datagrid,
    },
    {
        'AT_field_name': 'text',
        'DX_field_name': 'text',
        'DX_field_type': 'RichText',
    },
]

# ConditionsFields => IDPMTConstraints
fields_mapping_constraints = [
    {
        'AT_field_name': 'regional_constraints',
        'DX_field_name': 'regional_constraints',
    },
    {
        'AT_field_name': 'thematic_constraints',
        'DX_field_name': 'thematic_constraints',
    },
    {
        'AT_field_name': 'organizational_constraints',
        'DX_field_name': 'organizational_constraints',
    },
    {
        'AT_field_name': 'constraints',
        'DX_field_name': 'constraints',
        'DX_field_type': 'RichText',
    },
]

# RequestFields => IDPMTRequest
fields_mapping_request = [
    {
        'AT_field_name': 'startDate',
        'DX_field_name': 'startDate',
        'field_migrator': migrate_datetimefield,
    },
    {
        'AT_field_name': 'endDate',
        'DX_field_name': 'endDate',
        'field_migrator': migrate_datetimefield,
    },
    {
        'AT_field_name': 'constraints',
        'DX_field_name': 'constraints',
        'DX_field_type': 'RichText',
    },
    {
        'AT_field_name': 'ticketid',
        'DX_field_name': 'ticketid',
    },
]

# ResourceFields => IDPMTResource
fields_mapping_resource = [
    {
        'AT_field_name': 'compute_resources',
        'DX_field_name': 'compute_resources',
        'field_migrator': migrate_simple_datagrid,
    },
    {
        'AT_field_name': 'storage_resources',
        'DX_field_name': 'storage_resources',
        'field_migrator': migrate_simple_datagrid,
    },
]

# ResourceContextFields => IDPMTResourceContext
# only relations!
fields_mapping_resourcecontext = []


# content type migrators


def migrate_community(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'url',
            'DX_field_name': 'url',
        },
        {
            'AT_field_name': 'address',
            'DX_field_name': 'address',
            'field_migrator': migrate_adress,
        },
        {
            'AT_field_name': 'VAT',
            'DX_field_name': 'VAT',
        },
        {
            'AT_field_name': 'topics',
            'DX_field_name': 'topics',
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(fields_mapping, src_type='Community', dst_type='community_dx')


def migrate_downtime(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'startDateTime',
            'DX_field_name': 'start',
            'field_migrator': migrate_datetimefield,
        },
        {
            'AT_field_name': 'endDateTime',
            'DX_field_name': 'end',
            'field_migrator': migrate_datetimefield,
        },
        {
            'AT_field_name': 'reason',
            'DX_field_name': 'reason',
        },
        {
            'AT_field_name': 'severity',
            'DX_field_name': 'severity',
            'field_migrator': migrate_vocabulary,
        },
        {
            'AT_field_name': 'classification',
            'DX_field_name': 'classification',
            'field_migrator': migrate_vocabulary,
        },
    ]
    migrateCustomAT(fields_mapping, src_type='Downtime', dst_type='downtime_dx')


def migrate_environment(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'account',
            'DX_field_name': 'account',
        },
        {
            'AT_field_name': 'terms_of_use',
            'DX_field_name': 'terms_of_use',
        },
        {
            'AT_field_name': 'rootaccess',
            'DX_field_name': 'rootaccess',
        },
        {
            'AT_field_name': 'setup_procedure',
            'DX_field_name': 'setup_procedure',
        },
        {
            'AT_field_name': 'firewall_policy',
            'DX_field_name': 'firewall_policy',
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(fields_mapping, src_type='Environment', dst_type='environment_dx')


def migrate_name(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate ateapi.FormattableNameField to two fields"""
    name = src_obj.name
    dst_obj.firstname = name.get('firstname')
    dst_obj.lastname = name.get('lastname')


def migrate_phone(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate PhoneNumbersField to datagrid. Fieldnames do not match"""
    at_values = src_obj.getField(src_fieldname).get(src_obj)
    dx_values = []
    for at_value in at_values:
        if not at_value:
            continue
        dx_value = {}
        dx_value['number_type'] = at_value.get('type', 'Office')
        dx_value['number'] = at_value.get('number', None)
        dx_values.append(dx_value)
    setattr(dst_obj, dst_fieldname, dx_values)


def migrate_person(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'name',
            'DX_field_name': 'name',
            'field_migrator': migrate_name,
        },
        {
            'AT_field_name': 'email',
            'DX_field_name': 'email',
        },
        {
            'AT_field_name': 'phone',
            'DX_field_name': 'phone',
            'field_migrator': migrate_phone,
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(fields_mapping, src_type='Person', dst_type='person_dx')


def migrate_datetime_to_date(src_obj, dst_obj, src_fieldname, dst_fieldname):
    old_value = src_obj.getField(src_fieldname).get(src_obj)
    if not old_value:
        return
    new_value = old_value.asdatetime().date()
    setattr(dst_obj, dst_fieldname, new_value)


def migrate_project(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'website',
            'DX_field_name': 'website',
        },
        {
            'AT_field_name': 'start_date',
            'DX_field_name': 'start_date',
            'field_migrator': migrate_datetime_to_date,
        },
        {
            'AT_field_name': 'end_date',
            'DX_field_name': 'end_date',
            'field_migrator': migrate_datetime_to_date,
        },
        {
            'AT_field_name': 'call_for_collaboration',
            'DX_field_name': 'call_for_collaboration',
        },
        {
            'AT_field_name': 'uptake_plan',
            'DX_field_name': 'uptake_plan',
        },
        {
            'AT_field_name': 'repository',
            'DX_field_name': 'repository',
        },
        {
            'AT_field_name': 'topics',
            'DX_field_name': 'topics',
        },
        {
            'AT_field_name': 'scopes',
            'DX_field_name': 'scopes',
            'field_migrator': migrate_vocabulary,
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(fields_mapping, src_type='Project', dst_type='project_dx')


def migrate_provider(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'url',
            'DX_field_name': 'url',
        },
        {
            'AT_field_name': 'provider_type',
            'DX_field_name': 'provider_type',
        },
        {
            'AT_field_name': 'provider_userid',
            'DX_field_name': 'provider_userid',
        },
        {
            'AT_field_name': 'provider_status',
            'DX_field_name': 'provider_status',
        },
        {
            'AT_field_name': 'status_details',
            'DX_field_name': 'status_details',
        },
        {
            'AT_field_name': 'infrastructure',
            'DX_field_name': 'infrastructure',
        },
        {
            'AT_field_name': 'domain',
            'DX_field_name': 'domain',
        },
        {
            'AT_field_name': 'address',
            'DX_field_name': 'address',
            'field_migrator': migrate_adress,
        },
        {
            'AT_field_name': 'VAT',
            'DX_field_name': 'VAT',
        },
        {
            'AT_field_name': 'timezone',
            'DX_field_name': 'timezone',
        },
        {
            'AT_field_name': 'latitude',
            'DX_field_name': 'latitude',
        },
        {
            'AT_field_name': 'longitude',
            'DX_field_name': 'longitude',
        },
        {
            'AT_field_name': 'ip4range',
            'DX_field_name': 'ip4range',
        },
        {
            'AT_field_name': 'ip6range',
            'DX_field_name': 'ip6range',
        },
        {
            'AT_field_name': 'emergency_phone',
            'DX_field_name': 'emergency_phone',
        },
        {
            'AT_field_name': 'alarm_email',
            'DX_field_name': 'alarm_email',
        },
        {
            'AT_field_name': 'helpdesk_email',
            'DX_field_name': 'helpdesk_email',
        },
        {
            'AT_field_name': 'supported_os',
            'DX_field_name': 'supported_os',
        },
        {
            'AT_field_name': 'getAccount',
            'DX_field_name': 'getAccount',
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(fields_mapping, src_type='Provider', dst_type='provider_dx')


def migrate_registeredcomputeresource(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'hostname',
            'DX_field_name': 'hostname',
        },
        {
            'AT_field_name': 'ip',
            'DX_field_name': 'ip',
        },
        {
            'AT_field_name': 'cpus',
            'DX_field_name': 'cpus',
        },
        {
            'AT_field_name': 'memory',
            'DX_field_name': 'memory',
        },
        {
            'AT_field_name': 'localdisk',
            'DX_field_name': 'localdisk',
        },
        {
            'AT_field_name': 'virtualization',
            'DX_field_name': 'virtualization',
        },
        {
            'AT_field_name': 'os',
            'DX_field_name': 'os',
        },
        {
            'AT_field_name': 'software',
            'DX_field_name': 'software',
        },
    ]
    fields_mapping += fields_mapping_common + fields_mapping_resourcecontext
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredComputeResource',
        dst_type='registeredcomputeresource_dx',
    )


def migrate_registeredresource(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_resource + fields_mapping_resourcecontext
    migrateCustomAT(
        fields_mapping, src_type='RegisteredResource', dst_type='registeredresource_dx'
    )


def migrate_registeredservice(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'monitored',
            'DX_field_name': 'monitored',
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping, src_type='RegisteredService', dst_type='registeredservice_dx'
    )


def migrate_registeredservice(context=None):
    # fix fti.content_meta_type being 'Registered Service' with a space
    portal_types = api.portal.get_tool('portal_types')
    fti = portal_types.get('RegisteredService')
    if fti.content_meta_type != 'RegisteredService':
        fti._updateProperty('content_meta_type', 'RegisteredService')
    fields_mapping = [
        {
            'AT_field_name': 'monitored',
            'DX_field_name': 'monitored',
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping, src_type='RegisteredService', dst_type='registeredservice_dx'
    )


def migrate_registeredservicecomponent(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'service_type',
            'DX_field_name': 'service_type',
            'field_migrator': migrate_vocabulary,
        },
        {
            'AT_field_name': 'service_url',
            'DX_field_name': 'service_url',
        },
        {
            'AT_field_name': 'host_name',
            'DX_field_name': 'host_name',
        },
        {
            'AT_field_name': 'host_ip4',
            'DX_field_name': 'host_ip4',
        },
        {
            'AT_field_name': 'host_ip6',
            'DX_field_name': 'host_ip6',
        },
        {
            'AT_field_name': 'host_dn',
            'DX_field_name': 'host_dn',
        },
        {
            'AT_field_name': 'host_os',
            'DX_field_name': 'host_os',
        },
        {
            'AT_field_name': 'host_architecture',
            'DX_field_name': 'host_architecture',
        },
        {
            'AT_field_name': 'monitored',
            'DX_field_name': 'monitored',
        },
        {
            'AT_field_name': 'implementation_configuration',
            'DX_field_name': 'implementation_configuration',
            'field_migrator': migrate_simple_datagrid,
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredServiceComponent',
        dst_type='registeredservicecomponent_dx',
    )


def migrate_size(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate RecordField size to datagrid. storage_class does not match"""
    field = src_obj.getField(src_fieldname)
    if not field:
        return
    at_value = field.get(src_obj)
    if not at_value:
        return
    dx_value = {}
    dx_value['value'] = at_value.get('value', None)
    dx_value['unit'] = at_value.get('unit', None)
    dx_value['storage_class'] = at_value.get('storage class', None)
    setattr(dst_obj, dst_fieldname, [dx_value])


def migrate_registeredstorageresource(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'size',
            'DX_field_name': 'size',
            'field_migrator': migrate_size,
        },
        {
            'AT_field_name': 'max_objects',
            'DX_field_name': 'max_objects',
        },
        {
            'AT_field_name': 'cost_factor',
            'DX_field_name': 'cost_factor',
        },
    ]
    fields_mapping += fields_mapping_common + fields_mapping_resourcecontext
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredStorageResource',
        dst_type='registeredstorageresource_dx',
    )


def migrate_resourceoffer(context=None):
    fields_mapping = []
    fields_mapping += (
        fields_mapping_common + fields_mapping_resource + fields_mapping_constraints
    )
    migrateCustomAT(
        fields_mapping, src_type='ResourceOffer', dst_type='resourceoffer_dx'
    )


def migrate_resourcerequest(context=None):
    fields_mapping = []
    fields_mapping += (
        fields_mapping_common + fields_mapping_resource + fields_mapping_request
    )
    migrateCustomAT(
        fields_mapping, src_type='ResourceRequest', dst_type='resourcerequest_dx'
    )


def migrate_service(context=None):
    fields_mapping = [
        {
            'AT_field_name': 'description_internal',
            'DX_field_name': 'description_internal',
        },
        {
            'AT_field_name': 'url',
            'DX_field_name': 'url',
        },
        {
            'AT_field_name': 'service_area',
            'DX_field_name': 'service_area',
        },
        {
            'AT_field_name': 'service_type',
            'DX_field_name': 'service_type',
        },
        {
            'AT_field_name': 'value_to_customer',
            'DX_field_name': 'value_to_customer',
        },
        {
            'AT_field_name': 'value_to_customer',
            'DX_field_name': 'value_to_customer',
        },
        {
            'AT_field_name': 'funders_for_service',
            'DX_field_name': 'funders_for_service',
        },
        {
            'AT_field_name': 'request_procedures',
            'DX_field_name': 'request_procedures',
        },
        {
            'AT_field_name': 'helpdesk',
            'DX_field_name': 'helpdesk',
        },
        {
            'AT_field_name': 'service_complete_link',
            'DX_field_name': 'service_complete_link',
        },
        {
            'AT_field_name': 'competitors',
            'DX_field_name': 'competitors',
        },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(fields_mapping, src_type='Service', dst_type='service_dx')


def migrate_servicecomponent(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping, src_type='ServiceComponent', dst_type='servicecomponent_dx'
    )


def migrate_servicecomponentimplementation(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentImplementation',
        dst_type='servicecomponentimplementation_dx',
    )


def migrate_servicecomponentimplementationdetails(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentImplementationDetails',
        dst_type='servicecomponentimplementationdetails_dx',
    )


def migrate_servicecomponentoffer(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_constraints
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentOffer',
        dst_type='servicecomponentoffer_dx',
    )


def migrate_servicecomponentrequest(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_request
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentRequest',
        dst_type='servicecomponentrequest_dx',
    )


def migrate_serviceoffer(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_constraints
    migrateCustomAT(fields_mapping, src_type='ServiceOffer', dst_type='serviceoffer_dx')


def migrate_servicerequest(context=None):
    fields_mapping = []
    fields_mapping += (
        fields_mapping_common + fields_mapping_request + fields_mapping_resource
    )
    migrateCustomAT(
        fields_mapping, src_type='ServiceRequest', dst_type='servicerequest_dx'
    )
