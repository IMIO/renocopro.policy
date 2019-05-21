# -*- coding: utf-8 -*-
import os

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from eea.facetednavigation.layout.layout import FacetedLayout
from renocopro.policy.portlets.footer import add_portlets
from renocopro.policy.portlets.footer import delete_portlets

from renocopro.policy import _


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["renocopro.policy:uninstall"]


def post_install(context):
    """Post install script"""
    objects_to_remove = ("events", "news", "Members")
    portal = api.portal.get()
    for obj in objects_to_remove:
        if obj in portal:
            api.content.delete(obj=portal[obj])

    add_taxonomies()
    add_stucture(portal)
    add_portlets()
    delete_portlets()


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

    data_type_of_professional = {
        "taxonomy": "type_of_professional",
        "field_title": translate(
            _("Type of professional"), target_language=current_lang
        ),
        "field_description": "",
        "default_language": "fr",
        "filename": "taxonomy-settings-type-of-professional.xml",
    }

    portal = api.portal.get()
    sm = portal.getSiteManager()

    types_of_work_item = "collective.taxonomy.types_of_work"
    type_of_building_item = "collective.taxonomy.type_of_building"
    other_functions_item = "collective.taxonomy.other_functions"
    legal_status_item = "collective.taxonomy.legal_status"
    type_of_professional_item = "collective.taxonomy.type_of_professional"
    utility_types_of_work = sm.queryUtility(ITaxonomy, name=types_of_work_item)
    utility_type_of_building = sm.queryUtility(ITaxonomy, name=type_of_building_item)
    utility_other_functions = sm.queryUtility(ITaxonomy, name=other_functions_item)
    utility_legal_status = sm.queryUtility(ITaxonomy, name=legal_status_item)
    utility_type_of_professional = sm.queryUtility(
        ITaxonomy, name=type_of_professional_item
    )

    if (
        utility_types_of_work
        and utility_type_of_building
        and utility_other_functions
        and utility_legal_status
        and utility_type_of_professional
    ):
        return

    create_taxonomy_object(data_types_of_work)
    create_taxonomy_object(data_type_of_building)
    create_taxonomy_object(data_other_functions)
    create_taxonomy_object(data_legal_status)
    create_taxonomy_object_and_values(data_type_of_professional, portal)

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


def create_taxonomy_object_and_values(data_tax, portal):
    taxonomy = registerTaxonomy(
        api.portal.get(),
        name=data_tax["taxonomy"],
        title=data_tax["field_title"],
        description=data_tax["field_description"],
        default_language=data_tax["default_language"],
    )

    adapter = TaxonomyImportExportAdapter(portal)
    data_path = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_path, data_tax["filename"])
    data = (open(file_path, "r").read(),)
    import_file = data[0]
    adapter.importDocument(taxonomy, import_file)

    del data_tax["taxonomy"]
    del data_tax["filename"]
    taxonomy.registerBehavior(**data_tax)


def add_stucture(portal):
    # Folder case studies
    if "case-studies" not in portal:
        obj = create_content("Folder", _(u"Case studies"), portal)
        _activate_dashboard_navigation(obj, True, "/faceted/config/case_studies.xml")
        set_constrain_types(obj, ["case_studies", "Image", "File"])
        case_studies_layout = FacetedLayout(obj)
        case_studies_layout.update_layout(layout="faceted-casestudies")
        _publish(obj)

    # Folder professionals
    if "professionals" not in portal:
        obj = create_content("Folder", _(u"Professionals"), portal)
        _activate_dashboard_navigation(obj, True, "/faceted/config/professionals.xml")
        set_constrain_types(obj, ["professional", "Image", "File"])
        professional_layout = FacetedLayout(obj)
        professional_layout.update_layout(layout="faceted-professionals")
        _publish(obj)

    # Folder news
    if "news" not in portal:
        obj = create_content("Folder", _(u"News"), portal)
        _activate_dashboard_navigation(obj, True, "/faceted/config/news.xml")
        set_constrain_types(obj, ["News Item", "Image", "File"])
        news_layout = FacetedLayout(obj)
        news_layout.update_layout(layout="faceted-news")
        _publish(obj)


def add_behavior(type_name, behavior_name):
    """Add a behavior to a type"""
    fti = queryUtility(IDexterityFTI, name=type_name)
    if not fti:
        return
    behaviors = list(fti.behaviors)
    if behavior_name not in behaviors:
        behaviors.append(behavior_name)
    fti._updateProperty("behaviors", tuple(behaviors))


def _activate_dashboard_navigation(context, configuration=False, path=None):
    subtyper = context.restrictedTraverse("@@faceted_subtyper")
    if subtyper.is_faceted:
        return
    subtyper.enable()
    if configuration and path:
        context.unrestrictedTraverse("@@faceted_exportimport").import_xml(
            import_file=open(os.path.dirname(__file__) + path)
        )


def create_content(type_content, title, parent):
    new_obj = api.content.create(type=type_content, title=title, container=parent)
    return new_obj


def set_constrain_types(obj, list_contraint):
    behavior = ISelectableConstrainTypes(obj)
    behavior.setConstrainTypesMode(1)
    behavior.setImmediatelyAddableTypes(list_contraint)
    behavior.setLocallyAllowedTypes(list_contraint)


def _publish(obj):
    if api.content.get_state(obj) != "published":
        api.content.transition(obj, transition="publish")
