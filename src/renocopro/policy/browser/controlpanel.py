# -*- coding: utf-8 -*-

from renocopro.policy import _
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class IRenocoproSettingsSchema(Interface):

    profassional_manager_email = schema.TextLine(
        title=_(u"Email address of the professional manager"),
        description=_(
            u"If there are multiple email addresses, separate them with semicolons"
        ),
        rquired=False,
    )


class RenocoproSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IRenocoproSettingsSchema
    label = _(u"Configuration for renocopro product")
    description = _(u"")

    def updateFields(self):
        super(RenocoproSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(RenocoproSettingsEditForm, self).updateWidgets()


class RenocoproSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = RenocoproSettingsEditForm
