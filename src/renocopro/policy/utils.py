# -*- coding: utf-8 -*-
import os
import re
import unicodedata

import geopy
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from Products.CMFPlone.utils import safe_unicode
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from zope.component import getSiteManager
from zope.i18n import translate
from renocopro.policy import _


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


# Set up regular expressions
re_words = re.compile(r"<[^>]+?>|([^<>\s]+)", re.S)
re_chars = re.compile(r"<[^>]+?>|(.)", re.S)
re_tag = re.compile(r"<(/)?(\S+?)(?:(\s*/)|\s.*?)?>", re.S)
re_newlines = re.compile(r"\r\n|\r")  # Used in normalize_newlines
re_camel_case = re.compile(r"(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))")


class Truncator:
    """
    An object used to truncate text, either by characters or words.

    Based on https://github.com/django/django/blob/master/django/utils/text.py
    """

    def __init__(self, text):
        self.text = str(text)

    def add_truncation_text(self, text, truncate=None):
        if truncate is None:
            truncate = "…"
        if text.endswith(truncate):
            # Don't append the truncation text if the current text already
            # ends in this.
            return text
        return "%s%s" % (text, truncate)

    def chars(self, num, truncate=None, html=False):
        """
        Return the text truncated to be no longer than the specified number
        of characters.
        `truncate` specifies what should be used to notify that the string has
        been truncated, defaulting to a translatable string of an ellipsis.
        """
        length = int(num)
        text = unicodedata.normalize("NFC", self.text)

        # Calculate the length to truncate to (max length - end_text length)
        truncate_len = length
        for char in self.add_truncation_text("", truncate):
            if not unicodedata.combining(char):
                truncate_len -= 1
                if truncate_len == 0:
                    break
        if html:
            return self._truncate_html(length, truncate, text, truncate_len, False)
        return self._text_chars(length, truncate, text, truncate_len)

    def _text_chars(self, length, truncate, text, truncate_len):
        """Truncate a string after a certain number of chars."""
        s_len = 0
        end_index = None
        for i, char in enumerate(text):
            if unicodedata.combining(char):
                # Don't consider combining characters
                # as adding to the string length
                continue
            s_len += 1
            if end_index is None and s_len > truncate_len:
                end_index = i
            if s_len > length:
                # Return the truncated string
                return self.add_truncation_text(text[: end_index or 0], truncate)

        # Return the original string since no truncation was necessary
        return text

    def words(self, num, truncate=None, html=False):
        """
        Truncate a string after a certain number of words. `truncate` specifies
        what should be used to notify that the string has been truncated,
        defaulting to ellipsis.
        """
        length = int(num)
        if html:
            return self._truncate_html(length, truncate, self.text, length, True)
        return self._text_words(length, truncate)

    def _text_words(self, length, truncate):
        """
        Truncate a string after a certain number of words.
        Strip newlines in the string.
        """
        words = self.text.split()
        if len(words) > length:
            words = words[:length]
            return self.add_truncation_text(" ".join(words), truncate)
        return " ".join(words)

    def _truncate_html(self, length, truncate, text, truncate_len, words):
        """
        Truncate HTML to a certain number of chars (not counting tags and
        comments), or, if words is True, then to a certain number of words.
        Close opened tags if they were correctly closed in the given HTML.
        Preserve newlines in the HTML.
        """
        if words and length <= 0:
            return ""

        html4_singlets = (
            "br",
            "col",
            "link",
            "base",
            "img",
            "param",
            "area",
            "hr",
            "input",
        )

        # Count non-HTML chars/words and keep note of open tags
        pos = 0
        end_text_pos = 0
        current_len = 0
        open_tags = []

        regex = re_words if words else re_chars

        while current_len <= length:
            m = regex.search(text, pos)
            if not m:
                # Checked through whole string
                break
            pos = m.end(0)
            if m.group(1):
                # It's an actual non-HTML word or char
                current_len += 1
                if current_len == truncate_len:
                    end_text_pos = pos
                continue
            # Check for tag
            tag = re_tag.match(m.group(0))
            if not tag or current_len >= truncate_len:
                # Don't worry about non tags or tags after our truncate point
                continue
            closing_tag, tagname, self_closing = tag.groups()
            # Element names are always case-insensitive
            tagname = tagname.lower()
            if self_closing or tagname in html4_singlets:
                pass
            elif closing_tag:
                # Check for match in open tags list
                try:
                    i = open_tags.index(tagname)
                except ValueError:
                    pass
                else:
                    # SGML: An end tag closes, back to the matching start tag,
                    # all unclosed intervening start tags with omitted end tags
                    open_tags = open_tags[i + 1 :]
            else:
                # Add it to the start of the open tags list
                open_tags.insert(0, tagname)

        if current_len <= length:
            return text
        out = text[:end_text_pos]
        truncate_text = self.add_truncation_text("", truncate)
        if truncate_text:
            out += truncate_text
        # Close any tags still open
        for tag in open_tags:
            out += "</%s>" % tag
        # Return string
        return out


def send_registration_mail(event):
    lang = api.portal.get_current_language()[:2]
    email = event.object._login
    body = translate(
        _(
            u"email_registration_mail",
            default=u"""Hello,

Thank you for your registration and your interest in the Reno-Copro platform.

If you have any questions, please do not hesitate to contact us ( ace.retrofitting@liege.be).

Yours sincerely""",
        ),
        target_language=lang,
    )
    api.portal.send_email(
        recipient=email,
        subject=translate(_(u"Reno-copro registration"), target_language=lang),
        body=body,
    )
