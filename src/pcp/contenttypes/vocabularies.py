# -*- coding: utf-8 -*-
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

