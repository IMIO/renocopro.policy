# -*- coding: utf-8 -*-

from plone import schema
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from renocopro.policy import _
from zope.interface import implements


class IRealization(model.Schema):
    title = schema.TextLine(title=_(u"Name of the project"), required=True)

    fieldset(
        "address of the co-ownership",
        label=_(u"Address of the co-ownership"),
        fields=["street", "city", "zip_code"],
    )

    street = schema.TextLine(title=_(u"Street"), required=False)

    city = schema.TextLine(title=_(u"City"), required=False)

    zip_code = schema.Int(title=_(u"Zip code"), required=False)

    fieldset(
        "contact details of the syndic",
        label=_(u"Contact details of the syndic"),
        fields=["name", "email", "phone"],
    )

    name = schema.TextLine(title=_(u"Name"), required=False)

    email = schema.Email(title=_(u"Email"), required=False)

    phone = schema.TextLine(title=_(u"Phone / Mobile phone"), required=False)

    fieldset("other", label=_(u"Other"), fields=["rich_description", "innovative"])

    rich_description = RichText(
        title=_(u"Description of the work carried out"), required=False
    )

    innovative = RichText(
        title=_(u"Innovative aspects implemented"),
        description=_(
            u"Technical point of view, financing, management of the co-ownership"
        ),
        required=False,
    )


class Realization(Container):
    implements(IRealization)
