# -*- coding: utf-8 -*-
from plone import api
from plone.app.portlets.portlets import classic
from plone.app.portlets.portlets import navigation
from plone.app.textfield.value import RichTextValue
from plone.portlet.static import static
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from renocopro.policy.utils import getFileContent
from zope.component import getMultiAdapter
from zope.component import getUtility


def add_portlets():
    portal = api.portal.get()
    manager = getUtility(IPortletManager, name="plone.footerportlets", context=portal)
    mapping = getMultiAdapter((portal, manager), IPortletAssignmentMapping)

    if "partner" not in mapping.keys():
        mapping["partner"] = classic.Assignment(template="@@partners-portlet", macro="")

    if "navigation" not in mapping.keys():
        mapping["navigation"] = navigation.Assignment(
            name="Plan du site", topLevel=0  # this is tied to CSS classes
        )

    if "contact" not in mapping.keys():
        mapping["contact"] = static.Assignment(
            header="Informations de contact",  # this is tied to CSS classes
            text=RichTextValue(getFileContent("portlets/templates/contact.html")),
            omit_border=True,
        )

    if "infos" not in mapping.keys():
        mapping["infos"] = static.Assignment(
            header="Nos partenaires",  # this is tied to CSS classes
            text=RichTextValue(getFileContent("portlets/templates/infos.html")),
            omit_border=True,
        )

    if "legal" not in mapping.keys():
        mapping["legal"] = static.Assignment(
            header=u"Informations légales",  # this is tied to CSS classes
            text=RichTextValue(getFileContent("portlets/templates/legal.html")),
            omit_border=True,
        )


def delete_portlets():
    portal = api.portal.get()
    manager = getUtility(IPortletManager, name="plone.footerportlets", context=portal)
    mapping = getMultiAdapter((portal, manager), IPortletAssignmentMapping)
    portlets = ["footer", "colophon", "actions"]
    for portlet in portlets:
        if portlet in mapping.keys():
            del mapping[portlet]
