# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.standardtiles import PloneMessageFactory as _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from plone.tiles import Tile
from zope import schema
from renocopro.policy.utils import translate_selected_taxonomy_item
import random


class ICaseStudiesTile(model.Schema):
    """
    """

    title = schema.TextLine(title=_(u"Title"), required=False)

    folder = schema.Choice(
        title=_(u"Select the folder of cases studies"),
        required=False,
        vocabulary="plone.app.vocabularies.Catalog",
    )
    directives.widget(
        "folder",
        RelatedItemsFieldWidget,
        pattern_options={"selectableTypes": ["Folder"]},
    )

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Limit Search Results"),
        required=False,
        default=8,
        min=1,
    )

    limit_slider = schema.Int(
        title=_(u"Limit slider"),
        description=_(u"Number of element in slider"),
        required=False,
        default=4,
        min=1,
    )


class CaseStudiesTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile("templates/case_studies.pt")

    def __call__(self):
        return self.template()

    def contents(self):
        limit = self.data["limit"]
        catalog = api.portal.get_tool("portal_catalog")
        results = catalog(portal_type="case_studies", review_state="published")
        random_result = random.sample(results, len(results))
        return random_result[:limit]

    def title(self):
        return self.data["title"]

    def folder(self):
        uid = self.data["folder"]
        if uid:
            folder = api.content.get(UID=uid)
            return folder.absolute_url()
        return None

    def slider_limit(self):
        return self.data["limit_slider"]

    def slider_class(self):
        limit = self.data["limit_slider"]
        if limit == 1:
            return "slider flexslider-tile one"
        else:
            return "slider flexslider-tile multiple"

    def get_taxonomy_item(self, context, taxonomy_id, item_id):
        return translate_selected_taxonomy_item(context, taxonomy_id, item_id)
