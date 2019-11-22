# -*- coding: utf-8 -*-

from renocopro.policy import _
from plone import schema
from plone.app.users.browser.register import BaseRegistrationForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from plone.autoform.widgets import ParameterizedWidget
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEnhancedUserDataSchema(model.Schema):

    last_name = schema.TextLine(title=_(u"Last name"), required=False)
    first_name = schema.TextLine(title=_(u"First name"), required=False)
    email = schema.TextLine(title=_(u"Email"), required=True)


class UserSchemaExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.remove("email")
        self.remove("fullname")
        fields["email"].widgetFactory = ParameterizedWidget(
            None, placeholder=_(u"ex: dupont@email.com"), description=u""
        )
        fields["last_name"].widgetFactory = ParameterizedWidget(
            None, placeholder=_(u"ex: Dupont")
        )
        fields["first_name"].widgetFactory = ParameterizedWidget(
            None, placeholder=_(u"ex: Jean")
        )
        self.add(fields)
        self.move("last_name", before="*")
        self.move("first_name", after="last_name")
        self.move("email", after="first_name")


class UserDataPanelExtender(UserSchemaExtender):
    adapts(Interface, IDefaultBrowserLayer, UserDataPanel)


class RegistrationPanelExtender(UserSchemaExtender):
    adapts(Interface, IDefaultBrowserLayer, BaseRegistrationForm)

    def update(self):
        super(RegistrationPanelExtender, self).update()
        self.form.label = _(u"I create my account")
