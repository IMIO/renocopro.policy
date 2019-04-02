# -*- coding: utf-8 -*-
from renocopro.policy import _

from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["renocopro.policy:uninstall"]


def post_install(context):
    """Post install script"""
    add_taxonomies()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_taxonomies():
    current_lang = api.portal.get_current_language()[:2]

    data_types_of_work = {
        "taxonomy": "types_of_work",
        "field_title": translate(_("Types of work"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    data_type_of_building = {
        "taxonomy": "type_of_building",
        "field_title": translate(_("Type of building"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    data_other_functions = {
        "taxonomy": "other_functions",
        "field_title": translate(_("Other functions"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    data_legal_status = {
        "taxonomy": "legal_status",
        "field_title": translate(_("Legal status"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    portal = api.portal.get()
    sm = portal.getSiteManager()
    types_of_work_item = "collective.taxonomy.types_of_work"
    type_of_building_item = "collective.taxonomy.type_of_building"
    other_functions_item = "collective.taxonomy.other_functions"
    legal_status_item = "collective.taxonomy.legal_status"
    utility_types_of_work = sm.queryUtility(ITaxonomy, name=types_of_work_item)
    utility_type_of_building = sm.queryUtility(ITaxonomy, name=type_of_building_item)
    utility_other_functions = sm.queryUtility(ITaxonomy, name=other_functions_item)
    utility_legal_status = sm.queryUtility(ITaxonomy, name=legal_status_item)

    if (
        utility_types_of_work
        and utility_type_of_building
        and utility_other_functions
        and utility_legal_status
    ):
        return

    create_taxonomy_object(data_types_of_work)
    create_taxonomy_object(data_type_of_building)
    create_taxonomy_object(data_other_functions)
    create_taxonomy_object(data_legal_status)

    # remove taxonomy test
    item = "collective.taxonomy.test"
    utility = sm.queryUtility(ITaxonomy, name=item)
    if utility:
        utility.unregisterBehavior()
        sm.unregisterUtility(utility, ITaxonomy, name=item)
        sm.unregisterUtility(utility, IVocabularyFactory, name=item)
        sm.unregisterUtility(utility, ITranslationDomain, name=item)


def create_taxonomy_object(data_tax):
    taxonomy = registerTaxonomy(
        api.portal.get(),
        name=data_tax["taxonomy"],
        title=data_tax["field_title"],
        description=data_tax["field_description"],
        default_language=data_tax["default_language"],
    )

    del data_tax["taxonomy"]
    taxonomy.registerBehavior(**data_tax)
