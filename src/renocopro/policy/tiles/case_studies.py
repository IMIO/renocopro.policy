from plone.supermodel import model
from plone.tiles import Tile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import random


class ICaseStudiesTile(model.Schema):
    """
    """


class CaseStudiesTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile("templates/case_studies.pt")

    def __call__(self):
        return self.template()

    def contents(self):
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(portal_type='case_studies')
        random_results = random.sample(results, 4)
        return random_results
