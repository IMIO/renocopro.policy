# -*- coding: utf-8 -*-

from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.dexterity.browser.edit import DefaultEditForm
from renocopro.policy import _
from renocopro.policy.content.realization import IRealization
from renocopro.policy.utils import execute_under_admin
from z3c.form import button
from z3c.form.field import Fields
from z3c.form.form import EditForm
from z3c.form.group import Group, GroupForm


class DefaultGroup(Group):
    __name__ = "default"
    label = _(u"Default")
    fields = Fields(IRealization).select(
        "title", "contact_details_of_the_syndic", "rich_description", "innovative"
    )
    fields = fields + Fields(ILeadImage).select("image")


class AddressGroup(Group):
    __name__ = "address of the co-ownership"
    label = _(u"Address of the co-ownership")
    fields = Fields(IRealization).select("street", "city", "zip_code")


class RealizationForm(GroupForm, EditForm):

    groups = (DefaultGroup, AddressGroup)
    label = _(u"Realization")
    ignoreContext = True

    def update(self):
        super(RealizationForm, self).update()

    def send_request(self, data):
        container = self.context
        execute_under_admin(
            container,
            api.content.create,
            type="realization",
            title=data["title"],
            contact_details_of_the_syndic=data["contact_details_of_the_syndic"],
            rich_description=data["rich_description"],
            innovative=data["innovative"],
            street=data["street"],
            city=data["city"],
            zip_code=data["zip_code"],
            container=container,
            image=data["image"],
        )
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u"Send"), name="send")
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        self.send_request(data)


class RealizationEditForm(DefaultEditForm):
    pass
