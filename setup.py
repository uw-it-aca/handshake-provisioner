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
        "Django~=4.2",
        "django-storages[google, s3]",
        "urllib3<2",  # pinned for boto3
        "uw-person-client~=1.2",
        'uw-memcached-clients~=1.0',
        'UW-RestClients-Core~=1.4',
        'UW-RestClients-SWS~=2.4',
        "nameparser>=1.0.4,<2.0",
        "UW-Django-SAML2~=1.7",
        "lxml==4.9.4",
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
