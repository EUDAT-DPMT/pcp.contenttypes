# -*- coding: UTF-8 -*-
from collective.relationhelpers import api as relapi
from plone import api
from plone.app.contenttypes.migration.migration import migrateCustomAT
from Products.CMFPlone.utils import safe_text

import logging

log = logging.getLogger(__name__)

# Field Migrators

def migrate_adress(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate ateapi.AddressField to multiple dx fields
    """
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
                val = tuple(safe_unicode(i) for i in val)
            if isinstance(at_value, list):
                val = [safe_unicode(i) for i in val]
            dx_value[key] = val
        dx_values.append(dx_value)
    setattr(dst_obj, dst_fieldname, dx_values)


# Some AT fields have different names than the relationships!
FIELD_RELATIONSHIP_MAPPING = {
    'admins': 'community_admins',
    'community': 'done_for',
    'registered_services_used': 'using',
    'project_enabler': 'enabled_by',
    'admins': 'admin_of',
}

def migrate_relations(src_obj, dst_obj, src_fieldname, dst_fieldname):
    src_fieldname = FIELD_RELATIONSHIP_MAPPING.get(src_fieldname, src_fieldname)
    reference_catalog = api.portal.get_tool('reference_catalog')
    if not reference_catalog:
        return
    # During the migration the uid was already moved to dst_obj (=the dexterity target)!
    # That's why src_obj.getField(src_fieldname).get(src_obj) is empty!
    uid = dst_obj.UID()
    for brain in reference_catalog._optimizedQuery(
            uid=uid,
            indexname='sourceUID',
            relationship=src_fieldname):
        rel = brain.getObject()
        target = rel.getTargetObject()
        if not target:
            log.info(u'Warning: relation {} from {} to {} not migrated!'.format(
                rel.relationship, rel.sourceUID, rel.targetUID))
            continue
            # if not target:
            #     log.info(u'Warning: relation {} from {} to {} not migrated!'.format(
            #         rel.relationship, rel.sourceUID, rel.targetUID))
            #     continue
        relapi.link_objects(dst_obj, target, relationship=dst_fieldname)


# Field mappings for behaviors to inject into content-type mappings
# CommonFields => IDPMTCommon
fields_mapping_common = [
        {'AT_field_name': 'identifiers',
         'DX_field_name': 'identifiers',
         'field_migrator': migrate_simple_datagrid,
         },
        {'AT_field_name': 'additional',
         'DX_field_name': 'additional',
         'field_migrator': migrate_simple_datagrid,
         },
    ]

# ConditionsFields => IDPMTConstraints
fields_mapping_constraints = [
        {'AT_field_name': 'regional_constraints',
         'DX_field_name': 'regional_constraints',
         },
        {'AT_field_name': 'thematic_constraints',
         'DX_field_name': 'thematic_constraints',
         },
        {'AT_field_name': 'organizational_constraints',
         'DX_field_name': 'organizational_constraints',
         },
        {'AT_field_name': 'constraints',
         'DX_field_name': 'constraints',
         'dx_fieldtype': 'RichText',
         },
    ]

# RequestFields => IDPMTRequest
fields_mapping_request = [
        {'AT_field_name': 'startDate',
         'DX_field_name': 'startDate',
         'dx_fieldtype': 'Datetime',
         },
        {'AT_field_name': 'endDate',
         'DX_field_name': 'endDate',
         'dx_fieldtype': 'Datetime',
         },
        # {'AT_field_name': 'preferred_providers',
        #  'DX_field_name': 'preferred_providers',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'constraints',
         'DX_field_name': 'constraints',
         'dx_fieldtype': 'RichText',
         },
        {'AT_field_name': 'ticketid',
         'DX_field_name': 'ticketid',
         },
    ]

# ResourceFields => IDPMTResource
fields_mapping_resource = [
        {'AT_field_name': 'compute_resources',
         'DX_field_name': 'compute_resources',
         'field_migrator': migrate_simple_datagrid,
         },
        {'AT_field_name': 'storage_resources',
         'DX_field_name': 'storage_resources',
         'field_migrator': migrate_simple_datagrid,
         },
    ]

# ResourceContextFields => IDPMTResourceContext
fields_mapping_resourcecontext = [
        # {'AT_field_name': 'project',
        #  'DX_field_name': 'project',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'customer',
        #  'DX_field_name': 'customer',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'contact',
        #  'DX_field_name': 'contact',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'request',
        #  'DX_field_name': 'request',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'services',
        #  'DX_field_name': 'services',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'linked_resources',
        #  'DX_field_name': 'linked_resources',
        #  'field_migrator': migrate_relations,
        #  },
    ]


# content type migrators

def migrate_community(context=None):
    fields_mapping = [
        {'AT_field_name': 'url',
         'DX_field_name': 'url',
         },
        {'AT_field_name': 'address',
         'DX_field_name': 'address',
         'field_migrator': migrate_adress,
         },
        {'AT_field_name': 'VAT',
         'DX_field_name': 'VAT',
         },
        # {'AT_field_name': 'representative',
        #  'DX_field_name': 'representative',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'admins',
        #  'DX_field_name': 'community_admins',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'topics',
         'DX_field_name': 'topics',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Community',
        dst_type='community_dx')


def migrate_downtime(context=None):
    fields_mapping = [
        {'AT_field_name': 'startDateTime',
         'DX_field_name': 'start',
         'dx_fieldtype': 'Datetime',
         },
        {'AT_field_name': 'endDateTime',
         'DX_field_name': 'end',
         'dx_fieldtype': 'Datetime',
         },
        # {'AT_field_name': 'affected_registered_serivces',
        #  'DX_field_name': 'affected_registered_services',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'reason',
         'DX_field_name': 'reason',
         },
        {'AT_field_name': 'severity',
         'DX_field_name': 'severity',
         },
        {'AT_field_name': 'classification',
         'DX_field_name': 'classification',
         },
    ]
    migrateCustomAT(
        fields_mapping,
        src_type='Downtime',
        dst_type='downtime_dx')


def migrate_environment(context=None):
    fields_mapping = [
        # {'AT_field_name': 'contact',
        #  'DX_field_name': 'contact',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'account',
         'DX_field_name': 'account',
         },
        {'AT_field_name': 'terms_of_use',
         'DX_field_name': 'terms_of_use',
         },
        {'AT_field_name': 'rootaccess',
         'DX_field_name': 'rootaccess',
         },
        {'AT_field_name': 'setup_procedure',
         'DX_field_name': 'setup_procedure',
         },
        {'AT_field_name': 'firewall_policy',
         'DX_field_name': 'firewall_policy',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Environment',
        dst_type='environment_dx')


def migrate_name(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate ateapi.FormattableNameField to two fields
    """
    name = src_obj.name
    dst_obj.firstname = name.get('firstname')
    dst_obj.lastname = name.get('lastname')


def migrate_phone(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate PhoneNumbersField to datagrid. Fieldnames do not match
    """
    at_values = src_obj.getField(src_fieldname).get(src_obj)
    dx_values = []
    for at_value in at_values:
        if not at_value:
            continue
        dx_value = {}
        dx_value['number_type'] = at_value['type']
        dx_value['number'] = at_value['number']
        dx_values.append(dx_value)
    setattr(dst_obj, dst_fieldname, dx_values)


def migrate_person(context=None):
    fields_mapping = [
        {'AT_field_name': 'name',
         'DX_field_name': 'name',
         'field_migrator': migrate_name,
         },
        {'AT_field_name': 'email',
         'DX_field_name': 'email',
         },
        # {'AT_field_name': 'affiliation',
        #  'DX_field_name': 'affiliation',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'phone',
         'DX_field_name': 'phone',
         'field_migrator': migrate_phone,
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Person',
        dst_type='person_dx')


def migrate_datetime_to_date(src_obj, dst_obj, src_fieldname, dst_fieldname):
    old_value = src_obj.getField(src_fieldname).get(src_obj)
    if not old_value:
        return
    new_value = old_value.asdatetime().date()
    setattr(dst_obj, dst_fieldname, new_value)


def migrate_project(context=None):
    fields_mapping = [
        {'AT_field_name': 'website',
         'DX_field_name': 'website',
         },
        # {'AT_field_name': 'community',
        #  'DX_field_name': 'community',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'community_contact',
        #  'DX_field_name': 'community_contact',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'registered_services_used',
        #  'DX_field_name': 'registered_services_used',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'general_provider',
        #  'DX_field_name': 'general_provider',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'project_enabler',
        #  'DX_field_name': 'project_enabler',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'start_date',
         'DX_field_name': 'start_date',
         'field_migrator': migrate_datetime_to_date,
         },
        {'AT_field_name': 'end_date',
         'DX_field_name': 'end_date',
         'field_migrator': migrate_datetime_to_date,
         },
        {'AT_field_name': 'call_for_collaboration',
         'DX_field_name': 'call_for_collaboration',
         },
        {'AT_field_name': 'uptake_plan',
         'DX_field_name': 'uptake_plan',
         },
        {'AT_field_name': 'repository',
         'DX_field_name': 'repository',
         },
        {'AT_field_name': 'topics',
         'DX_field_name': 'topics',
         },
        {'AT_field_name': 'scopes',
         'DX_field_name': 'scopes',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Project',
        dst_type='project_dx')


def migrate_provider(context=None):
    fields_mapping = [
        {'AT_field_name': 'url',
         'DX_field_name': 'url',
         },
        {'AT_field_name': 'provider_type',
         'DX_field_name': 'provider_type',
         },
        {'AT_field_name': 'provider_userid',
         'DX_field_name': 'provider_userid',
         },
        {'AT_field_name': 'provider_status',
         'DX_field_name': 'provider_status',
         },
        {'AT_field_name': 'status_details',
         'DX_field_name': 'status_details',
         },
        {'AT_field_name': 'infrastructure',
         'DX_field_name': 'infrastructure',
         },
        {'AT_field_name': 'domain',
         'DX_field_name': 'domain',
         },
        {'AT_field_name': 'address',
         'DX_field_name': 'address',
         'field_migrator': migrate_adress,
         },
        {'AT_field_name': 'VAT',
         'DX_field_name': 'VAT',
         },
        {'AT_field_name': 'timezone',
         'DX_field_name': 'timezone',
         },
        {'AT_field_name': 'latitude',
         'DX_field_name': 'latitude',
         },
        {'AT_field_name': 'longitude',
         'DX_field_name': 'longitude',
         },
        {'AT_field_name': 'ip4range',
         'DX_field_name': 'ip4range',
         },
        {'AT_field_name': 'ip6range',
         'DX_field_name': 'ip6range',
         },
        # {'AT_field_name': 'contact',
        #  'DX_field_name': 'contact',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'business_contact',
        #  'DX_field_name': 'business_contact',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'security_contact',
        #  'DX_field_name': 'security_contact',
        #  'field_migrator': migrate_relations,
        #  },
        # {'AT_field_name': 'admins',
        #  'DX_field_name': 'admins',
        #  'field_migrator': migrate_relations,
        #  },
        {'AT_field_name': 'emergency_phone',
         'DX_field_name': 'emergency_phone',
         },
        {'AT_field_name': 'alarm_email',
         'DX_field_name': 'alarm_email',
         },
        {'AT_field_name': 'helpdesk_email',
         'DX_field_name': 'helpdesk_email',
         },
        {'AT_field_name': 'supported_os',
         'DX_field_name': 'supported_os',
         },
        {'AT_field_name': 'getAccount',
         'DX_field_name': 'getAccount',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Provider',
        dst_type='provider_dx')


def migrate_registeredcomputeresource(context=None):
    fields_mapping = [
        {'AT_field_name': 'hostname',
         'DX_field_name': 'hostname',
         },
        {'AT_field_name': 'ip',
         'DX_field_name': 'ip',
         },
        {'AT_field_name': 'cpus',
         'DX_field_name': 'cpus',
         },
        {'AT_field_name': 'memory',
         'DX_field_name': 'memory',
         },
        {'AT_field_name': 'localdisk',
         'DX_field_name': 'localdisk',
         },
        {'AT_field_name': 'virtualization',
         'DX_field_name': 'virtualization',
         },
        {'AT_field_name': 'os',
         'DX_field_name': 'os',
         },
        {'AT_field_name': 'software',
         'DX_field_name': 'software',
         },
    ]
    fields_mapping += fields_mapping_common + fields_mapping_resourcecontext
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredComputeResource',
        dst_type='registeredcomputeresource_dx')


def migrate_registeredresource(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_resource + fields_mapping_resourcecontext
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredResource',
        dst_type='registeredresource_dx')


def migrate_registeredservice(context=None):
    fields_mapping = [
        {'AT_field_name': 'monitored',
         'DX_field_name': 'monitored',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredService',
        dst_type='registeredservice_dx')



def migrate_registeredservice(context=None):
    # fix fti.content_meta_type being 'Registered Service' with a space
    portal_types = api.portal.get_tool('portal_types')
    fti = portal_types.get('RegisteredService')
    if fti.content_meta_type != 'RegisteredService':
        fti._updateProperty('content_meta_type', 'RegisteredService')
    fields_mapping = [
        {'AT_field_name': 'monitored',
         'DX_field_name': 'monitored',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredService',
        dst_type='registeredservice_dx')


def migrate_registeredservicecomponent(context=None):
    fields_mapping = [
        {'AT_field_name': 'service_type',
         'DX_field_name': 'service_type',
         },
        {'AT_field_name': 'service_url',
         'DX_field_name': 'service_url',
         },
        {'AT_field_name': 'host_name',
         'DX_field_name': 'host_name',
         },
        {'AT_field_name': 'host_ip4',
         'DX_field_name': 'host_ip4',
         },
        {'AT_field_name': 'host_ip6',
         'DX_field_name': 'host_ip6',
         },
        {'AT_field_name': 'host_dn',
         'DX_field_name': 'host_dn',
         },
        {'AT_field_name': 'host_os',
         'DX_field_name': 'host_os',
         },
        {'AT_field_name': 'host_architecture',
         'DX_field_name': 'host_architecture',
         },
        {'AT_field_name': 'monitored',
         'DX_field_name': 'monitored',
         },
        {'AT_field_name': 'implementation_configuration',
         'DX_field_name': 'implementation_configuration',
         'field_migrator': migrate_simple_datagrid,
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredServiceComponent',
        dst_type='registeredservicecomponent_dx')


def migrate_size(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate RecordField size to datagrid. storage_class does not match
    """
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
        {'AT_field_name': 'size',
         'DX_field_name': 'size',
         'field_migrator': migrate_size,
         },
        {'AT_field_name': 'max_objects',
         'DX_field_name': 'max_objects',
         },
        {'AT_field_name': 'cost_factor',
         'DX_field_name': 'cost_factor',
         'dx_fieldtype': 'Datetime',
         },
    ]
    fields_mapping += fields_mapping_common + fields_mapping_resourcecontext
    migrateCustomAT(
        fields_mapping,
        src_type='RegisteredStorageResource',
        dst_type='registeredstorageresource_dx')


def migrate_resourceoffer(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_resource + fields_mapping_constraints
    migrateCustomAT(
        fields_mapping,
        src_type='ResourceOffer',
        dst_type='resourceoffer_dx')


def migrate_resourcerequest(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_resource + fields_mapping_request
    migrateCustomAT(
        fields_mapping,
        src_type='ResourceRequest',
        dst_type='resourcerequest_dx')


def migrate_service(context=None):
    fields_mapping = [
        {'AT_field_name': 'description_internal',
         'DX_field_name': 'description_internal',
         },
        {'AT_field_name': 'url',
         'DX_field_name': 'url',
         },
        {'AT_field_name': 'service_area',
         'DX_field_name': 'service_area',
         },
        {'AT_field_name': 'service_type',
         'DX_field_name': 'service_type',
         },
        {'AT_field_name': 'value_to_customer',
         'DX_field_name': 'value_to_customer',
         },
        {'AT_field_name': 'value_to_customer',
         'DX_field_name': 'value_to_customer',
         },
        {'AT_field_name': 'funders_for_service',
         'DX_field_name': 'funders_for_service',
         },
        {'AT_field_name': 'request_procedures',
         'DX_field_name': 'request_procedures',
         },
        {'AT_field_name': 'helpdesk',
         'DX_field_name': 'helpdesk',
         },
        {'AT_field_name': 'service_complete_link',
         'DX_field_name': 'service_complete_link',
         },
        {'AT_field_name': 'competitors',
         'DX_field_name': 'competitors',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Service',
        dst_type='service_dx')


def migrate_servicecomponent(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponent',
        dst_type='servicecomponent_dx')


def migrate_servicecomponentimplementation(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentImplementation',
        dst_type='servicecomponentimplementation_dx')


def migrate_servicecomponentimplementationdetails(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentImplementationDetails',
        dst_type='servicecomponentimplementationdetails_dx')


def migrate_servicecomponentoffer(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_constraints
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentOffer',
        dst_type='servicecomponentoffer_dx')


def migrate_servicecomponentrequest(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_request
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceComponentRequest',
        dst_type='servicecomponentrequest_dx')


# def migrate_servicedetails(context=None):
#     fields_mapping = []
#     fields_mapping += fields_mapping_common + fields_mapping_request
#     migrateCustomAT(
#         fields_mapping,
#         src_type='ServiceDetails',
#         dst_type='servicedetails_dx')


def migrate_serviceoffer(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_constraints
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceOffer',
        dst_type='serviceoffer_dx')


def migrate_servicerequest(context=None):
    fields_mapping = []
    fields_mapping += fields_mapping_common + fields_mapping_request + fields_mapping_resource
    migrateCustomAT(
        fields_mapping,
        src_type='ServiceRequest',
        dst_type='servicerequest_dx')
