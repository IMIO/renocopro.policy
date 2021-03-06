# -*- coding: utf-8 -*-
from plone import api
from renocopro.policy import _
from renocopro.policy import logger
from zope.i18n import translate


def send_notification(obj, event):
    fields = []

    if event.descriptions:
        for modif in event.descriptions[0].attributes:
            fields.append(modif)

    if not fields:
        return

    lang = api.portal.get_current_language()[:2]
    email = api.portal.get_registry_record(
        "renocopro.policy.browser.controlpanel.IRenocoproSettingsSchema.professional_manager_email",
        default=None,
    )
    if email is None:
        logger.warn("missing email for professional notification")
        return

    list_mail = email.split(";")

    body = translate(
        _(
            u"email_body_professionnal_modification",
            default=u"""The professional ${name} received modifications in the fields:
          ${fields}

          you can access it at the following url:
          ${url}
          """,
            mapping={
                u"url": obj.absolute_url(),
                u"name": obj.title,
                u"fields": ", ".join(fields),
            },
        ),
        target_language=lang,
    )
    for mail in list_mail:
        api.portal.send_email(
            recipient=mail,
            subject=translate(
                _(u"New professionnal modification"), target_language=lang
            ),
            body=body,
        )
