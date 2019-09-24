# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from Products.CMFPlone.utils import safe_unicode

from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from zope.component import getSiteManager

import os
import geopy


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """

    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()


def execute_under_admin(portal, function, *args, **kwargs):
    """ Execude code under admin privileges """
    sm = getSecurityManager()
    try:
        try:
            tmp_user = UnrestrictedUser("admin", "", [""], "")
            # Wrap the user in the acquisition context of the portal
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)
            # Call the function
            return function(*args, **kwargs)
        except:  # noqa
            # If special exception handlers are needed, run them here
            raise
    finally:
        # Restore the old security manager
        setSecurityManager(sm)


def getFileContent(file_path):
    package_path = os.path.dirname(__file__)
    filePath = "/".join([package_path, file_path])
    f = file(filePath)  # noqa
    data = safe_unicode(f.read())
    f.close()
    return data


def get_location_info(address):
    location = None
    try:
        geolocator = geopy.geocoders.Nominatim()
        location = geolocator.geocode(address, exactly_one=True)
    except:  # noqa
        pass
    return location


def translate_selected_taxonomy_item(context, taxonomy_id, item_id):
    sm = getSiteManager()
    utility = sm.queryUtility(ITaxonomy, name=taxonomy_id)
    if item_id:
        if item_id:
            return utility.translate(
                item_id,
                context=context,
                target_language=api.portal.get_current_language()[:2],
            )
