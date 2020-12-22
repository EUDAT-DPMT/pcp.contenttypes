# -*- coding: utf-8 -*-
from pcp.contenttypes.content_dx.common import unit_map
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory


@provider(IVocabularyFactory)
def identifier_types(context):
    name = 'dpmt.identifier_types'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def storage_types(context):
    name = 'dpmt.storage_types'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def operating_systems(context):
    name = 'dpmt.operating_systems'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def provider_types(context):
    name = 'dpmt.provider_types'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def provider_stati(context):
    name = 'dpmt.provider_stati'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def country_names(context):
    name = 'dpmt.country_names'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def information_units(context):
    units = unit_map.keys()
    return safe_simplevocabulary_from_values(sorted(units))


@provider(IVocabularyFactory)
def downtime_classes(context):
    name = 'dpmt.downtime_classes'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def scope_vocabulary(context):
    name = 'dpmt.scope_vocabulary'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def service_types(context):
    name = 'dpmt.service_types'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def severity_levels(context):
    name = 'dpmt.severity_levels'
    values = api.portal.get_registry_record(name)
    return safe_simplevocabulary_from_values(values)
