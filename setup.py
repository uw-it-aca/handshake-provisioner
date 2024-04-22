#!/usr/bin/env python

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/handshake-provisioner>`_.
"""

version_path = "sis_provisioner/VERSION"
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="handshake-provisioner",
    version=VERSION,
    packages=["sis_provisioner"],
    include_package_data=True,
    install_requires=[
        "django~=4.2",
        "django-storages[google, s3]",
        "urllib3<2",  # pinned for boto3
        "django-person-client~=1.0",
        "uw-memcached-clients~=1.0",
        "uw-restclients-core~=1.4",
        "uw-restclients-sws~=2.4",
        "nameparser>=1.0.4,<2.0",
        "uw-django-saml2~=1.8",
        "lxml<5",
        "xmlsec==1.3.13"
    ],
    license="Apache License, Version 2.0",
    description="UW application that supports Handshake",
    long_description=README,
    url="https://github.com/uw-it-aca/handshake-provisioner",
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
