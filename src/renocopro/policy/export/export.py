# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
from collective.excelexport.exportables.dexterityfields import TextFieldRenderer
from collective.excelexport.exportables.dexterityfields import CollectionFieldRenderer
from collective.excelexport.interfaces import IExportable
from plone import api
from plone.app.textfield import RichTextValue
from plone.app.textfield.interfaces import IRichText
from plone.formwidget.geolocation.interfaces import IGeolocation
from renocopro.policy.interfaces import IRenocoproPolicyLayer
from z3c.form.interfaces import NO_VALUE
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IObject
from zope.schema.interfaces import IText


class ObjectFieldRenderer(BaseFieldRenderer):
    adapts(IObject, Interface, Interface)

    def render_value(self, obj):
        values = self.get_value(obj)
        if IGeolocation.providedBy(values):
            if getattr(obj, "longitude", None) or getattr(obj, "latitude", None):
                return u"{0}/{1}".format(
                    getattr(obj, "longitude", ""), getattr(obj, "latitude", "")
                )


class FullTextFieldRenderer(TextFieldRenderer):
    adapts(IText, Interface, IRenocoproPolicyLayer)

    def render_value(self, obj):
        """Gets the value to render in excel file from content value
        """
        value = self.get_value(obj)
        if not value or value == NO_VALUE:
            return ""

        text = safe_unicode(self._get_text(value))

        return text


class FullRichTextFieldRenderer(FullTextFieldRenderer):
    adapts(IRichText, Interface, IRenocoproPolicyLayer)

    def _get_text(self, value):

        ptransforms = api.portal.get_tool("portal_transforms")
        return ptransforms.convert("html_to_text", value.output).getData().strip()


class RenocoproCollectionFieldRenderer(CollectionFieldRenderer):

    adapts(ICollection, Interface, IRenocoproPolicyLayer)

    separator = u"\n"

    def render_value(self, obj):
        """Gets the value to render in excel file from content value
        """
        value = self.get_value(obj)
        value_type = self.field.value_type
        if not value_type:
            value_type = self.field

        sub_renderer = getMultiAdapter(
            (value_type, self.context, self.request), interface=IExportable
        )
        try:
            val = []
            for v in value:
                val.append(v)
                if isinstance(v, RichTextValue):
                    ptransforms = api.portal.get_tool("portal_transforms")
                    val.append(
                        ptransforms.convert("html_to_text", v.output).getData().strip()
                    )
            if val:
                value = val
        except TypeError:
            pass
        try:
            return (
                value
                and self.separator.join(
                    [sub_renderer.render_collection_entry(obj, v) for v in value]
                )
                or u""
            )
        except TypeError:
            return value and self.separator.join([v for v in value]) or u""
