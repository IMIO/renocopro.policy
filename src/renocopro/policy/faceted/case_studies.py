# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory


class CaseStudiesView(BrowserView):

    def get_types_of_work_by_token(self, token):
        factory = getUtility(IVocabularyFactory, "collective.taxonomy.types_of_work")
        vocabulary = factory(self.context)
        try:
            return translate(vocabulary.getTerm(token).title, context=self.context)
        except KeyError:
            return

    def get_type_of_building_by_token(self, token):
        factory = getUtility(IVocabularyFactory, "collective.taxonomy.type_of_building")
        vocabulary = factory(self.context)
        try:
            return translate(vocabulary.getTerm(token).title, context=self.context)
        except KeyError:
            return
