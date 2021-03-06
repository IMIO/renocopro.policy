# -*- coding: utf-8 -*-
"""Installer for the renocopro.policy package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="renocopro.policy",
    version="1.0a25.dev0",
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="imio",
    author_email="support@imio.be",
    url="https://pypi.python.org/pypi/renocopro.policy",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["renocopro"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.restapi",
        "plone.app.dexterity",
        "collective.taxonomy",
        "plone.formwidget.geolocation",
        "collective.documentation",
        "plone.app.mosaic",
        "iaweb.mosaic",
        "eea.facetednavigation",
        "collective.behavior.gallery",
        "renocopro.theme",
        "collective.behavior.banner",
        "collective.easyform",
        "collective.defaultexcludedfromnav",
        "geopy",
        "collective.geolocationbehavior",
        "collective.faceted.map",
        "collective.recaptcha",
        "plone.formwidget.recaptcha",
        "imio.gdpr",
        "Products.PasswordStrength",
        "collective.excelexport",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = renocopro.policy.locales.update:update_locale
    """,
)
