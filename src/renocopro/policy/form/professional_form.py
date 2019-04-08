# -*- coding: utf-8 -*-

from z3c.form import button
from z3c.form.field import Fields
from z3c.form.group import Group, GroupForm
from z3c.form.form import EditForm
from renocopro.policy.content.professional import IProfessional
from plone import api
from zope.i18n import translate
from renocopro.policy import _
from renocopro.policy.utils import execute_under_admin


class DefaultGroup(Group):
    __name__ = "default"
    label = _(u"Default")
    fields = Fields(IProfessional).select(
        "title", "legal_status", "rich_description", "location"
    )


class ContactGroup(Group):
    __name__ = "contact person"
    label = _(u"Contact person")
    fields = Fields(IProfessional).select(
        "last_name",
        "first_name",
        "street",
        "city",
        "zip_code",
        "phone",
        "email",
        "website",
        "vat",
    )


class ActivityGroup(Group):
    __name__ = "activities"
    label = _(u"activities")
    fields = Fields(IProfessional).select("activity")


class ProfessionalForm(GroupForm, EditForm):

    groups = (DefaultGroup, ContactGroup, ActivityGroup)
    label = _(u"Professional")
    ignoreContext = True

    def send_mail(self, url):
        lang = api.portal.get_current_language()[:2]

        body = translate(
            _(
                u"email_body_professional_submission",
                default=u"""A new professional has been created you can access it at the following url:
              ${url}
              """,
                mapping={u"url": url},
            ),
            target_language=lang,
        )

        api.portal.send_email(
            recipient="foo@bar.com",
            subject=translate(_(u"New professional submission"), target_language=lang),
            body=body,
        )

    def send_request(self, data):
        container = api.portal.get()["professionals"]
        professional_obj = execute_under_admin(
            container,
            api.content.create,
            type="professional",
            title=data["title"],
            legal_status=data["legal_status"],
            rich_description=data["rich_description"],
            location=data["location"],
            last_name=data["last_name"],
            first_name=data["first_name"],
            street=data["street"],
            city=data["city"],
            zip_code=data["zip_code"],
            phone=data["phone"],
            email=data["email"],
            website=data["website"],
            vat=data["vat"],
            activity=data["activity"],
            container=container,
        )
        self.request.response.redirect(professional_obj.absolute_url())
        self.send_mail(professional_obj.absolute_url())

    @button.buttonAndHandler(_(u"Send"), name="send")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.send_request(data)
