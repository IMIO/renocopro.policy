# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from renocopro.policy.content.professional import IProfessional


@indexer(IProfessional)
def latitude(obj):
    return obj.location.latitude


@indexer(IProfessional)
def longitude(obj):
    return obj.location.longitude
