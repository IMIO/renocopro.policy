# -*- coding: utf-8 -*-

from renocopro.policy.user_schema import IEnhancedUserDataSchema
from plone.app.users.browser.account import AccountPanelSchemaAdapter


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema

    def _setProperty(self, name, value):
        result = super(EnhancedUserDataSchemaAdapter, self)._setProperty(name, value)
        if name in ("first_name", "last_name"):
            fullname = u"{0} {1}".format(
                self._getProperty("first_name"), self._getProperty("last_name")
            )
            self._set_fullname(fullname)
        return result

    def _set_fullname(self, value):
        return self.context.setMemberProperties({"fullname": value}, force_empty=True)
