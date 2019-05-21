# -*- coding: utf-8 -*-

from plone import api
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import ISingleCheckBoxWidget
from z3c.form.browser.checkbox import SingleCheckBoxWidget
from zope.interface import implementer_only


class IPolicySingleCheckBoxWidget(ISingleCheckBoxWidget):
    """interface for PolicySingleCheckBoxWidget"""


@implementer_only(IPolicySingleCheckBoxWidget)
class PolicySingleCheckBoxWidget(SingleCheckBoxWidget):
    def get_policy_link(self):
        return api.portal.get_registry_record(
            "renocopro.policy.browser.controlpanel.IRenocoproSettingsSchema.policy_link",
            default=None,
        )


def policy_single_checkbox_field_widget(field, request):
    """IFieldWidget factory for CheckBoxWidget."""
    return FieldWidget(field, PolicySingleCheckBoxWidget(request))
