# -*- coding: utf-8 -*-
from zope.component import provideAdapter
from zope.component import adapts
from zope.schema.interfaces import IInt
from z3c.form.interfaces import ITextWidget
from z3c.form.converter import IntegerDataConverter


class NoFormatIntegerDataConverter(IntegerDataConverter):

    adapts(IInt, ITextWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u""
        return unicode(value)  # noqa


provideAdapter(NoFormatIntegerDataConverter)
