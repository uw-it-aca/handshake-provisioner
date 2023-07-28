#!/usr/bin/env python

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/handshake-provisioner>`_.
"""

version_path = 'sis_provisioner/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='handshake-provisioner',
    version=VERSION,
    packages=['sis_provisioner'],
    include_package_data=True,
    install_requires = [
        'Django~=3.2',
        'django-storages[google]>=1.10',
        'boto3',
        #'axdd-person-client>=1.1.8,<1.2',
        'nameparser>=1.0.4,<2.0',
        'UW-Django-SAML2~=1.7',
    ],
    license='Apache License, Version 2.0',
    description='UW application that supports Handshake',
    long_description=README,
    url='https://github.com/uw-it-aca/handshake-provisioner',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
)
