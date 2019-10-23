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
            return truncator.words(20, "<div>...</div>", html=True)

    def get_activities(self, pro):
        activities = getattr(pro, "activity", [])
        parent = ""
        childs = []
        activities_dict = {}
        for activity in activities:
            if u"\xbb" in self.get_taxonomy_item(
                self.context, "collective.taxonomy.type_of_professional", activity
            ):
                if (
                    self.get_taxonomy_item(
                        self.context,
                        "collective.taxonomy.type_of_professional",
                        activity,
                    ).split(u"\xbb")[0]
                    == parent
                ):
                    childs.append(
                        self.get_taxonomy_item(
                            self.context,
                            "collective.taxonomy.type_of_professional",
                            activity,
                        ).split(u"\xbb")[1]
                    )
                    activities_dict[parent] = childs
                else:
                    if parent:
                        activities_dict[parent] = childs
                    childs = []
                    parent = self.get_taxonomy_item(
                        self.context,
                        "collective.taxonomy.type_of_professional",
                        activity,
                    ).split(u"\xbb")[0]
                    childs.append(
                        self.get_taxonomy_item(
                            self.context,
                            "collective.taxonomy.type_of_professional",
                            activity,
                        ).split(u"\xbb")[1]
                    )
                    activities_dict[parent] = childs
            else:
                activities_dict[
                    self.get_taxonomy_item(
                        self.context,
                        "collective.taxonomy.type_of_professional",
                        activity,
                    )
                ] = []

        structure = u""
        for parent in [[k, v] for k, v in activities_dict.items()]:
            if parent[1]:
                childs = u""
                for child in parent[1]:
                    childs = u"{0}<li>{1}</li>".format(childs, child)
                structure = u"{0}<li>{1}:<ul>{2}</ul></li>".format(
                    structure, parent[0], childs
                )
            else:
                structure = u"{0}<li>{1}</li>".format(structure, parent[0])
        return structure
