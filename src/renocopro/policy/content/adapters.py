# -*- coding: utf-8 -*-
from renocopro.policy.content.professional import DEFAULT_GEOLOCATION
from zope.interface import Interface


class IMapsConfiguration(Interface):
    pass


class MapsConfiguration(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def default_location(self):
        return DEFAULT_GEOLOCATION
