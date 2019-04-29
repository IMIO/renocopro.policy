# -*- coding: utf-8 -*-

from plone import schema
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.formwidget.geolocation.field import GeolocationField
from plone.supermodel import model
from renocopro.policy import _
from zope.interface import implements
from plone.supermodel.directives import fieldset


class IProfessional(model.Schema):

    title = schema.TextLine(title=_(u"Name of the company/organization"), required=True)

    legal_status = schema.Choice(
        title=_(u"Legal status"),
        vocabulary=u"collective.taxonomy.legal_status",
        required=False,
    )

    rich_description = RichText(
        title=_(u"Description of the company's activity"), required=False
    )

    location = GeolocationField(title=_(u"Location"), required=False)

    fieldset(
        "contact person",
        label=_(u"Contact person"),
        fields=[
            "last_name",
            "first_name",
            "street",
            "city",
            "zip_code",
            "phone",
            "email",
            "website",
            "vat",
        ],
    )

    last_name = schema.TextLine(title=_(u"Last name"), required=False)

    first_name = schema.TextLine(title=_(u"First name"), required=False)

    street = schema.TextLine(title=_(u"Street"), required=False)

    city = schema.TextLine(title=_(u"City"), required=False)

    zip_code = schema.Int(title=_(u"Zip code"), required=False)

    phone = schema.TextLine(
        title=_(u"Phone / Mobile phone of the contact person"), required=False
    )

    email = schema.Email(title=_(u"Email of the contact person"), required=False)

    website = schema.TextLine(title=_(u"website"), required=False)

    vat = schema.TextLine(title=_(u"VAT"), required=False)

    fieldset("activities", label=_(u"activities"), fields=["activity"])

    activity = schema.Choice(
        title=_(u"Specific activities in the field of condominium renovation"),
        vocabulary=u"collective.taxonomy.type_of_professional",
        required=False,
    )


class Professional(Container):
    implements(IProfessional)
