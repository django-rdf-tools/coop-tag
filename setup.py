#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

VERSION = __import__('coop_tag').__version__

import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='coop-tag',
    version = VERSION,
    description='Add-on for django-coop for managing tags with django-taggit',
    packages=[  'coop_tag', 'coop_tag.migrations'],
    include_package_data=True,
    author='Cooperative Quinode',
    author_email='contact@quinode.fr',
    license='BSD',
    zip_safe=False,
    install_requires = ['django-taggit==0.9.3','django-positions==0.4.3'],
    long_description = open('README.rst').read(),
    url = 'https://github.com/quinode/coop-tag/',
    download_url = 'https://github.com/quinode/coop-tag/tarball/master',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Natural Language :: English',
        'Natural Language :: French',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],

)

