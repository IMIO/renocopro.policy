# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from plone import schema
from plone import api
from plone.app.textfield import RichText
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.supermodel.directives import fieldset
from zope.component import getSiteManager
from zope.interface import implements
from renocopro.policy import _
from renocopro.policy.content.interfaces import IRenocopro


class ICaseStudies(IRenocopro):
    """ICaseStudies"""

    title = schema.TextLine(title=_(u"Title"), required=True)

    rich_description = RichText(title=_(u"Description"), required=False)

    fieldset(
        "building identity form",
        label=_(u"Building identity form"),
        fields=[
            "location",
            "types_of_work",
            "type_of_building",
            "renovation_year",
            "duration_of_the_work",
            "net_surface_area",
            "cost_of_renovation",
            "cost_m2",
            "number_of_housing_units",
            "number_of_coowners",
            "other_functions",
        ],
    )

    location = schema.TextLine(title=_(u"Location"), required=False)

    types_of_work = schema.Choice(
        title=_(u"Types of work"),
        vocabulary=u"collective.taxonomy.types_of_work",
        required=False,
    )

    type_of_building = schema.Choice(
        title=_(u"Type of building"),
        vocabulary=u"collective.taxonomy.type_of_building",
        required=False,
    )

    construction_year = schema.TextLine(title=_(u"Construction year"), required=False)

    renovation_year = schema.TextLine(title=_(u"Renovation year"), required=False)

    duration_of_the_work = schema.TextLine(
        title=_(u"Duration of the work"), required=False
    )

    net_surface_area = schema.TextLine(title=_(u"Heated floor area"), required=False)

    cost_of_renovation = schema.TextLine(title=_(u"Cost of renovation"), required=False)

    cost_m2 = schema.TextLine(title=_(u"Cost/m2"), required=False)

    number_of_housing_units = schema.TextLine(
        title=_(u"Number of housing units"), required=False
    )

    number_of_coowners = schema.TextLine(
        title=_(u"Number of co-owners"), required=False
    )

    other_functions = schema.Choice(
        title=_(u"Other functions"),
        vocabulary=u"collective.taxonomy.other_functions",
        required=False,
    )

    fieldset(
        "Other",
        label=_(u"Other"),
        fields=[
            "grants_and_subsidies",
            "financing_option",
            "actor",
            "work",
            "human_relations",
            "description_of_the_systems",
            "renewable_energies",
            "sustainable_aspects",
        ],
    )

    grants_and_subsidies = RichText(title=_(u"Grants and subsidies"), required=False)

    financing_option = RichText(title=_(u"Financing option"), required=False)

    actor = RichText(title=_(u"Actor"), required=False)

    work = RichText(
        title=_(u"Work"), description=_(u"Listing of all work done"), required=False
    )

    human_relations = RichText(
        title=_(u"Human relations"),
        description=_(
            u"Describe the decision-making methods, levers and obstacles related to condominium decision-making"
        ),
        required=False,
    )

    description_of_the_systems = RichText(
        title=_(u"Description of the systems"),
        description=_(u"heating, DHW, ventilation, possible cooling"),
        required=False,
    )

    renewable_energies = RichText(title=_(u"Renewable energies"), required=False)

    sustainable_aspects = RichText(title=_(u"Sustainable aspects"), required=False)


class CaseStudies(Container):
    implements(ICaseStudies)


class CaseStudiesView(DefaultView):
    def show_section(self):
        if (
            self.context.rich_description
            or self.context.grants_and_subsidies
            or self.context.financing_option
            or self.context.actor
            or self.context.human_relations
            or self.context.work
            or self.context.description_of_the_systems
            or self.context.renewable_energies
            or self.context.sustainable_aspects
        ):
            return True
        return False

    def translate_selected_taxonomy_item(self, context, taxonomy_id, item_id):
        sm = getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=taxonomy_id)
        if item_id:
            if item_id:
                return utility.translate(
                    item_id,
                    context=context,
                    target_language=api.portal.get_current_language()[:2],
                )
