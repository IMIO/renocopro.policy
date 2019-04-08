# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase


class CaseStudieViewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/case_studie_viewlet.pt")

    def get_cases(self):
        results = self.context.portal_catalog(
            type_of_building=self.context.type_of_building
        )
        brains = []
        for brain in results:
            if brain.getURL() != self.context.absolute_url():
                brains.append(brain)
        return brains