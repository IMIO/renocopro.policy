# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
import zope.interface


class IProfessionalRegistration(zope.interface.Interface):
    pass


class CaseStudieViewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/case_studie_viewlet.pt")

    def get_cases(self):
        if not self.context.type_of_building:
            return []
        results = self.context.portal_catalog(
            type_of_building=self.context.type_of_building
        )
        brains = []
        for brain in results:
            if brain.getURL() != self.context.absolute_url():
                brains.append(brain)
        return brains


class ProfessionalRegistrationViewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/professionnal_registration_viewlet.pt")

    def show_viewlet(self):
        if IProfessionalRegistration.providedBy(self.context):
            return True
        return False


class ProfessionalActionsViewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/professional_control_viewlet.pt")

    @property
    def is_professional(self):
        return self.context.portal_type == "professional"
