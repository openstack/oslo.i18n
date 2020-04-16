# Copyright 2012 Red Hat, Inc.
# Copyright 2013 IBM Corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""gettextutils provides a wrapper around gettext for OpenStack projects
"""

import copy
import gettext
import locale
import os

from oslo_i18n import _factory
from oslo_i18n import _locale

__all__ = [
    'install',
    'get_available_languages',
]


def install(domain):
    """Install a _() function using the given translation domain.

    Given a translation domain, install a _() function using gettext's
    install() function.

    The main difference from gettext.install() is that we allow
    overriding the default localedir (e.g. /usr/share/locale) using
    a translation-domain-specific environment variable (e.g.
    NOVA_LOCALEDIR).

    :param domain: the translation domain
    """
    from six import moves
    tf = _factory.TranslatorFactory(domain)
    moves.builtins.__dict__['_'] = tf.primary


_AVAILABLE_LANGUAGES = {}


def get_available_languages(domain):
    """Lists the available languages for the given translation domain.

    :param domain: the domain to get languages for
    """
    if domain in _AVAILABLE_LANGUAGES:
        return copy.copy(_AVAILABLE_LANGUAGES[domain])

    localedir = os.environ.get(_locale.get_locale_dir_variable_name(domain))

    def find(x):
        return gettext.find(domain, localedir=localedir, languages=[x])

    # NOTE(mrodden): en_US should always be available (and first in case
    # order matters) since our in-line message strings are en_US
    language_list = ['en_US']
    locale_identifiers = set(locale.windows_locale.values())
    language_list.extend(
        language for language in locale_identifiers if find(language)
    )

    _AVAILABLE_LANGUAGES[domain] = language_list
    return copy.copy(language_list)


_original_find = gettext.find
_FIND_CACHE = {}


def cached_find(domain, localedir=None, languages=None, all=0):
    """A version of gettext.find using a cache.

    gettext.find looks for mo files on the disk using os.path.exists. Those
    don't tend to change over time, but the system calls pile up with a
    long-running service. This caches the result so that we return the same mo
    files, and only call find once per domain.
    """
    key = (domain,
           localedir,
           tuple(languages) if languages is not None else None,
           all)
    if key in _FIND_CACHE:
        return _FIND_CACHE[key]
    result = _original_find(domain, localedir, languages, all)
    _FIND_CACHE[key] = result
    return result


gettext.find = cached_find
