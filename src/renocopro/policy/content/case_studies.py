# -*- coding: utf-8 -*-

from renocopro.policy import _

from plone import schema
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope.interface import implements


class ICaseStudies(model.Schema):
    """ICaseStudies"""

    title = schema.TextLine(title=_(u"Title"), required=True)

    description = RichText(title=_(u"Description"), required=False)

    fieldset(
        "building identity form",
        label=_(u"Building identity form"),
        fields=[
            "longitude",
            "latitude",
            "types_of_work",
            "type_of_building",
            "renovation_year",
            "duration_of_the_work",
            "net_surface_area",
            "cost_of_renovation",
            "cost_m2",
            "number_of_housing_units",
            "other_functions",
        ],
    )

    longitude = schema.Float(title=_(u"Longitude"), required=False)

    latitude = schema.Float(title=_(u"Latitude"), required=False)

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

    renovation_year = schema.Int(title=_(u"Renovation year"), required=False)

    duration_of_the_work = schema.Int(title=_(u"Duration of the work"), required=False)

    net_surface_area = schema.Int(title=_(u"Net surface area"), required=False)

    cost_of_renovation = schema.Int(title=_(u"Cost of renovation"), required=False)

    cost_m2 = schema.Int(title=_(u"Cost/m2"), required=False)

    number_of_housing_units = schema.Int(
        title=_(u"Number of housing units"), required=False
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
            "work",
            "human_relations",
            "energy",
            "enr_systems",
            "environment",
            "products",
            "costs",
        ],
    )

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

    energy = RichText(
        title=_(u"Energy"),
        description=_(
            u"Consumption, type of system implemented, performance achieved,... "
        ),
        required=False,
    )

    enr_systems = RichText(
        title=_(u"EnR & Systems"),
        description=_(u"Heating, ecs, cooling, ventilation, EnR"),
        required=False,
    )

    environment = RichText(
        title=_(u"Environment"),
        description=_(u"Vegetation, water management"),
        required=False,
    )

    products = RichText(title=_(u"Products"), required=False)

    costs = RichText(
        title=_(u"Cost"), description=_(u"Details of the big posts"), required=False
    )


class CaseStudies(Container):
    implements(ICaseStudies)
