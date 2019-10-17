# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from renocopro.policy.utils import Truncator
from renocopro.policy.utils import translate_selected_taxonomy_item


class ProfessionalsView(BrowserView):
    def get_taxonomy_item(self, context, taxonomy_id, item_id):
        return translate_selected_taxonomy_item(context, taxonomy_id, item_id)

    def get_rich_description(self, pro):
        if pro.rich_description:
            truncator = Truncator(pro.rich_description.output.encode("utf8"))
            return truncator.words(20, '<div>...</div>', html=True)
