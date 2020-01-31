# -*- coding: utf-8 -*-
from zope import schema
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from renocopro.policy import _
from z3c.form.form import Form
from zope.interface import implements
from z3c.form.field import Fields
from z3c.form.interfaces import IFieldsForm
from z3c.form import button
from plone import api
from renocopro.policy.utils import execute_under_admin


class IImageRea(model.Schema):
    title = schema.TextLine(title=_(u"Title"), required=True)
    description = schema.Text(title=_(u"Description"), required=False)
    image = NamedBlobImage(title=_(u"Image"), required=True)


class ImageForm(Form):

    label = _(u"Add image")
    implements(IFieldsForm)
    fields = Fields(IImageRea).select("title", "description", "image")

    ignoreContext = True

    def send_request(self, data):
        container = self.context
        execute_under_admin(
            container,
            api.content.create,
            type="Image",
            title=data["title"],
            image=data["image"],
            description=data["description"],
            container=container,
        )
        self.request.response.redirect(self.context.aq_parent.absolute_url())

    @button.buttonAndHandler(_(u"Send"), name="send")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.send_request(data)
