# -*- coding: utf-8 -*-

from plone import schema
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.formwidget.geolocation.field import GeolocationField
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import implements

from renocopro.policy import _
from renocopro.policy.utils import get_location_info
from renocopro.policy.utils import translate_selected_taxonomy_item

DEFAULT_GEOLOCATION = (50.6451381, 5.5734203)


class IProfessional(model.Schema):

    title = schema.TextLine(title=_(u"Name of the company/organization"), required=True)

    legal_status = schema.Choice(
        title=_(u"Legal status"),
        vocabulary=u"collective.taxonomy.legal_status",
        required=False,
    )

    rich_description = RichText(
        title=_(u"Description of the company's activity"),
        description=_(u"Summarize the activities of your company"),
        required=False,
    )

    specific_activities = RichText(
        title=_(u"Description of specific activities"),
        description=_(
            u"Describe the specific activities in the field of condominium renovation"
        ),
        required=False,
    )

    location = GeolocationField(title=_(u"Location"), required=False)

    fieldset(
        "contact person",
        label=_(u"Contact person"),
        fields=["last_name", "first_name", "phone", "email"],
    )

    last_name = schema.TextLine(title=_(u"Last name"), required=False)

    first_name = schema.TextLine(title=_(u"First name"), required=False)

    number = schema.TextLine(title=_(u"Number"), required=False)

    street = schema.TextLine(title=_(u"Street"), required=False)

    city = schema.TextLine(title=_(u"City"), required=False)

    zip_code = schema.Int(title=_(u"Zip code"), required=False)

    phone = schema.TextLine(
        title=_(u"Phone / Mobile phone of the contact person"), required=False
    )

    email = schema.Email(title=_(u"Email of the contact person"), required=False)

    website = schema.URI(title=_(u"website"), required=False)

    vat = schema.TextLine(title=_(u"VAT"), required=False)

    form.widget(activity=CheckBoxFieldWidget)
    activity = schema.List(
        title=_(u"Specific activities in the field of condominium renovation"),
        value_type=schema.Choice(
            title=_(u"Specific activities in the field of condominium renovation"),
            vocabulary=u"collective.taxonomy.type_of_professional",
        ),
        required=False,
    )


class Professional(Container):
    implements(IProfessional)


def handle_location(obj, event):

    if (obj.location.latitude, obj.location.longitude) != DEFAULT_GEOLOCATION:
        return

    address = u"{0} {1} {2} {3}".format(obj.number, obj.street, obj.zip_code, obj.city)
    obj.location = get_location_info(address)


class ProfessionalView(DefaultView):
    def get_taxonomy_item(self, context, taxonomy_id, item_id):
        return translate_selected_taxonomy_item(context, taxonomy_id, item_id)

    def get_realizations(self):
        brains = api.content.find(
            context=self.context,
            depth=1,
            portal_type="realization",
            sort_on="getObjPositionInParent",
        )
        return [b.getObject() for b in brains]

    def get_images(self, realization):
        brains = api.content.find(
            context=realization,
            depth=1,
            portal_type="Image",
            sort_on="getObjPositionInParent",
        )
        return [b.getObject() for b in brains]

    def get_info_real(self, real):
        title = real.title
        description = real.rich_description
        address = self.pretty_address("", real.street, real.city, real.zip_code)

        syndic = real.contact_details_of_the_syndic
        innovative = real.innovative

        structure = "<h3>{0}</h3>".format(title)
        if description:
            structure = '{0}<div class="description">{1}</div>'.format(
                structure, description.output
            )

        if syndic:
            structure = '{0}<div class="syndic"><label>{1}</label><p>{2}</p></div>'.format(
                structure, _(u"Contact details of the syndic"), syndic
            )

        if address:
            structure = '{0}<div class="address"><label>{1}</label><p>{2}</p></div>'.format(
                structure, _(u"Address of the co-ownership"), address
            )

        if innovative:
            structure = '{0}<div class="innovative"><label>{1}</label><div>{2}</div></div>'.format(
                structure, _(u"Innovative aspects implemented"), innovative.output
            )

        return structure

    def pretty_address(self, num, street, city, zip_code):
        address = ""
        if street or city or zip_code:
            if street and city and zip_code:
                address = "{0}, {1}({2})".format(street, city, zip_code)
            if street and city and not zip_code:
                address = "{0}, {1}".format(street, city)
            if not street and city and zip_code:
                address = "{0}({1})".format(city, zip_code)
            if street and not city and zip_code:
                address = "{0} ({1})".format(street, zip_code)
            if street and not city and not zip_code:
                address = street
            if not street and city and not zip_code:
                address = city
            if not street and not city and zip_code:
                address = zip_code
        if num:
            if address:
                address = "{0}, {1}".format(num, address)
            else:
                address = num
        return address

    def pretty_contact(self, last_name, first_name):
        return ("{0} {1}".format(last_name, first_name)).lstrip()
