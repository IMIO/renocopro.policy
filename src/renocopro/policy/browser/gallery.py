# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api


class GalleryView(BrowserView):
    """ A viewlet which renders the gallery """

    def get_photos(self):
        brains = api.content.find(
            context=self.context,
            depth=1,
            portal_type="Image",
            sort_on="getObjPositionInParent",
        )
        return [
            obj
            for obj in [b.getObject() for b in brains]
            if getattr(obj, "add_on_gallery", False)
        ]

    def image_url(self, obj, default_scale="preview"):
        url = ""
        images = obj.restrictedTraverse("@@images")
        image = images.scale("image", scale=default_scale)
        if image:
            url = image.url
        return url
