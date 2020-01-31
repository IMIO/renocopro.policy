# -*- coding: utf-8 -*-

from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.dexterity.browser.edit import DefaultEditForm
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from renocopro.policy import _
from renocopro.policy.content.realization import IRealization
from renocopro.policy.utils import execute_under_admin
from z3c.form import button
from z3c.form.field import Fields
from z3c.form.form import EditForm
from z3c.form.group import Group, GroupForm
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant


class IImagesRea(model.Schema):
    title1 = schema.TextLine(title=_(u"Title Image 1"), required=False)
    description1 = schema.Text(title=_(u"Description Image 1"), required=False)
    image1 = NamedBlobImage(title=_(u"Image 1"), required=False)

    title2 = schema.TextLine(title=_(u"Title Image 2"), required=False)
    description2 = schema.Text(title=_(u"Description Image 2"), required=False)
    image2 = NamedBlobImage(title=_(u"Image 2"), required=False)

    title3 = schema.TextLine(title=_(u"Title Image 3"), required=False)
    description3 = schema.Text(title=_(u"Description Image 3"), required=False)
    image3 = NamedBlobImage(title=_(u"Image 3"), required=False)

    title4 = schema.TextLine(title=_(u"Title Image 4"), required=False)
    description4 = schema.Text(title=_(u"Description Image 4"), required=False)
    image4 = NamedBlobImage(title=_(u"Image 4"), required=False)

    title5 = schema.TextLine(title=_(u"Title Image 5"), required=False)
    description5 = schema.Text(title=_(u"Description Image 5"), required=False)
    image5 = NamedBlobImage(title=_(u"Image 5"), required=False)

    title6 = schema.TextLine(title=_(u"Title Image 6"), required=False)
    description6 = schema.Text(title=_(u"Description Image 6"), required=False)
    image6 = NamedBlobImage(title=_(u"Image 6"), required=False)

    title7 = schema.TextLine(title=_(u"Title Image 7"), required=False)
    description7 = schema.Text(title=_(u"Description Image 7"), required=False)
    image7 = NamedBlobImage(title=_(u"Image 7"), required=False)

    title8 = schema.TextLine(title=_(u"Title Image 8"), required=False)
    description8 = schema.Text(title=_(u"Description Image 8"), required=False)
    image8 = NamedBlobImage(title=_(u"Image 8"), required=False)

    title9 = schema.TextLine(title=_(u"Title Image 9"), required=False)
    description9 = schema.Text(title=_(u"Description Image 9"), required=False)
    image9 = NamedBlobImage(title=_(u"Image 9"), required=False)

    title10 = schema.TextLine(title=_(u"Title Image 10"), required=False)
    description10 = schema.Text(title=_(u"Description Image 10"), required=False)
    image10 = NamedBlobImage(title=_(u"Image 10"), required=False)

    @invariant
    def address_invariant(data):
        if (
            ((data.image1 and not data.title1) or (data.title1 and not data.image1))
            or ((data.image2 and not data.title2) or (data.title2 and not data.image2))
            or ((data.image3 and not data.title3) or (data.title3 and not data.image3))
            or ((data.image4 and not data.title4) or (data.title4 and not data.image4))
            or ((data.image5 and not data.title5) or (data.title5 and not data.image5))
            or ((data.image6 and not data.title6) or (data.title6 and not data.image6))
            or ((data.image7 and not data.title7) or (data.title7 and not data.image7))
            or ((data.image8 and not data.title8) or (data.title8 and not data.image8))
            or ((data.image9 and not data.title9) or (data.title9 and not data.image9))
            or (
                (data.image10 and not data.title10)
                or (data.title10 and not data.image10)
            )
        ):
            raise Invalid(_(u"An image must contain at least one title and one file"))


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


class ImagesRealGroup(Group):
    __name__ = "images realization"
    label = _(u"Images of the realization")
    fields = Fields(IImagesRea)


class RealizationForm(GroupForm, EditForm):

    groups = (DefaultGroup, AddressGroup, ImagesRealGroup)
    label = _(u"Realization")
    ignoreContext = True

    def update(self):
        self.groups[0].fields.items()[-1][1].field.required = True
        super(RealizationForm, self).update()

    def add_image(self, container, image, title, description):
        execute_under_admin(
            container,
            api.content.create,
            type="Image",
            title=title,
            image=image,
            description=description,
            container=container,
        )

    def send_request(self, data):
        container = self.context
        real = execute_under_admin(
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
        if data["image1"]:
            self.add_image(real, data["image1"], data["title1"], data["description1"])
        if data["image2"]:
            self.add_image(real, data["image2"], data["title2"], data["description2"])
        if data["image3"]:
            self.add_image(real, data["image3"], data["title3"], data["description3"])
        if data["image4"]:
            self.add_image(real, data["image4"], data["title4"], data["description4"])
        if data["image5"]:
            self.add_image(real, data["image5"], data["title5"], data["description5"])
        if data["image6"]:
            self.add_image(real, data["image6"], data["title6"], data["description6"])
        if data["image7"]:
            self.add_image(real, data["image7"], data["title7"], data["description7"])
        if data["image8"]:
            self.add_image(real, data["image8"], data["title8"], data["description8"])
        if data["image9"]:
            self.add_image(real, data["image9"], data["title9"], data["description9"])
        if data["image10"]:
            self.add_image(
                real, data["image10"], data["title10"], data["description10"]
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
