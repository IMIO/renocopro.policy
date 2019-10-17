# -*- coding: utf-8 -*-

from renocopro.policy import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IAddOnTheGallery(model.Schema):

    add_on_gallery = schema.Bool(title=_(u"Add on the gallery"), required=False)


@implementer(IAddOnTheGallery)
@adapter(IDexterityContent)
class AddOnTheGallery(object):
    def __init__(self, context):
        self.context = context
