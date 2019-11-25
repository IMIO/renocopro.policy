# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api


class RegistrationInformationView(BrowserView):
    def go_to_registration(self):

        if api.user.is_anonymous():
            self.request.response.redirect(
                "{0}/@@professional_connection".format(api.portal.get().absolute_url())
            )
        else:
            self.request.response.redirect(
                "{0}/@@professional_form".format(api.portal.get().absolute_url())
            )
