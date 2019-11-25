# -*- coding: utf-8 -*-

from borg.localrole.interfaces import ILocalRoleProvider
from renocopro.policy.content.professional import DEFAULT_GEOLOCATION
from zope.interface import Interface
from zope.interface import implements


class IMapsConfiguration(Interface):
    pass


class MapsConfiguration(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def default_location(self):
        return DEFAULT_GEOLOCATION


class LocalRoleAdapter(object):
    implements(ILocalRoleProvider)

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal):
        """Grant permission for principal"""
        allowed_users = getattr(self.context, "allowed_users", []) or []
        if principal in allowed_users:
            return ("Reader", "Professional Editor")
        return []

    def getAllRoles(self):
        """Grant permissions"""
        if not getattr(self.context, "allowed_users", None):
            yield ("", ("",))
            raise StopIteration
        else:
            permissions = ("Reader", "Professional Editor")
            for allowed_user in self.context.allowed_users:
                yield (allowed_user, permissions)
