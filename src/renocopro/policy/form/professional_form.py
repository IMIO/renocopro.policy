# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from plone import api
from plone.supermodel import model
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from renocopro.policy import _
from renocopro.policy import logger
from renocopro.policy.content.professional import IProfessional
from renocopro.policy.fields.policy_checkbox import policy_single_checkbox_field_widget
from renocopro.policy.utils import execute_under_admin
from z3c.form import button
from z3c.form.field import Fields
from z3c.form.form import EditForm
from z3c.form.group import Group, GroupForm
from zope import schema
from zope.i18n import translate
from zope.component import getMultiAdapter


class IValidation(model.Schema):
    validation = schema.Bool(title=_(u"Validation"))

    captcha = schema.TextLine(description=u"", required=False)


class DefaultGroup(Group):
    __name__ = "default"
    label = _(u"Default")
    fields = Fields(IProfessional).select(
        "title",
        "legal_status",
        "rich_description",
        "location",
        "activity",
        "street",
        "number",
        "city",
        "zip_code",
        "website",
        "vat",
    )
    fields = fields + Fields(ILeadImage).select("image")
    fields = fields + Fields(IValidation).select("validation")
    fields = fields + Fields(IValidation).select("captcha")

    fields["captcha"].widgetFactory = ReCaptchaFieldWidget
    fields["validation"].widgetFactory = policy_single_checkbox_field_widget


class ContactGroup(Group):
    __name__ = "contact person"
    label = _(u"Contact person")
    fields = Fields(IProfessional).select("last_name", "first_name", "phone", "email")


class ProfessionalForm(GroupForm, EditForm):

    groups = (DefaultGroup, ContactGroup)
    label = _(u"Professional")

    _required_fields = (
        "title",
        "street",
        "number",
        "city",
        "number",
        "zip_code",
        "vat",
        "activity",
        "validation",
        "last_name",
        "first_name",
        "phone",
    )
    ignoreContext = True

    def update(self):
        for group in self.groups:
            for name, field in group.fields.items():
                field.field.required = name in self._required_fields
        super(ProfessionalForm, self).update()

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

        lang = api.portal.get_current_language()[:2]
        email = api.portal.get_registry_record(
            "renocopro.policy.browser.controlpanel.IRenocoproSettingsSchema.professional_manager_email",
            default=None,
        )
        if email is None:
            logger.warn("missing email for professional notification")
            return

        list_mail = email.split(";")
        for mail in list_mail:
            api.portal.send_email(
                recipient=mail,
                subject=translate(
                    _(u"New professional submission"), target_language=lang
                ),
                body=body,
            )

    def send_request(self, data):
        container = api.portal.get()["professionnels"]
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
            number=data["number"],
            city=data["city"],
            zip_code=data["zip_code"],
            phone=data["phone"],
            email=data["email"],
            website=data["website"],
            vat=data["vat"],
            image=data["image"],
            activity=data["activity"],
            container=container,
            allowed_users=[api.user.get_current().getId()],
        )
        self.request.response.redirect(
            "{0}/@@confirm".format(api.portal.get().absolute_url())
        )
        self.send_mail(professional_obj.absolute_url())

    @button.buttonAndHandler(_(u"Send"), name="send")
    def handleApply(self, action):
        captcha = getMultiAdapter(
            (aq_inner(self.context), self.request), name="recaptcha"
        )
        if captcha.verify():
            data, errors = self.extractData()
            if data.get("validation"):
                if errors:
                    self.status = self.formErrorsMessage
                    return

                self.send_request(data)
            else:
                IStatusMessage(self.request).addStatusMessage(
                    _(u"You must validate the policy"), "error"
                )
        else:
            IStatusMessage(self.request).addStatusMessage(
                _(u"Captcha incorrect"), "captcha"
            )
