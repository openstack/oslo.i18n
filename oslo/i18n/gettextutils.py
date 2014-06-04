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
import os

from babel import localedata
import six

# Expose a few internal pieces as part of our public API.
from oslo.i18n._factory import TranslatorFactory  # noqa
from oslo.i18n._lazy import enable_lazy  # noqa
from oslo.i18n._translate import translate  # noqa


def install(domain):
    """Install a _() function using the given translation domain.

    Given a translation domain, install a _() function using gettext's
    install() function.

    The main difference from gettext.install() is that we allow
    overriding the default localedir (e.g. /usr/share/locale) using
    a translation-domain-specific environment variable (e.g.
    NOVA_LOCALEDIR).

    :param domain: the translation domain
    :param lazy: indicates whether or not to install the lazy _() function.
                 The lazy _() introduces a way to do deferred translation
                 of messages by installing a _ that builds Message objects,
                 instead of strings, which can then be lazily translated into
                 any available locale.
    """
    from six import moves
    tf = TranslatorFactory(domain)
    moves.builtins.__dict__['_'] = tf.primary


_AVAILABLE_LANGUAGES = {}


def get_available_languages(domain):
    """Lists the available languages for the given translation domain.

    :param domain: the domain to get languages for
    """
    if domain in _AVAILABLE_LANGUAGES:
        return copy.copy(_AVAILABLE_LANGUAGES[domain])

    localedir = '%s_LOCALEDIR' % domain.upper()
    find = lambda x: gettext.find(domain,
                                  localedir=os.environ.get(localedir),
                                  languages=[x])

    # NOTE(mrodden): en_US should always be available (and first in case
    # order matters) since our in-line message strings are en_US
    language_list = ['en_US']
    # NOTE(luisg): Babel <1.0 used a function called list(), which was
    # renamed to locale_identifiers() in >=1.0, the requirements master list
    # requires >=0.9.6, uncapped, so defensively work with both. We can remove
    # this check when the master list updates to >=1.0, and update all projects
    list_identifiers = (getattr(localedata, 'list', None) or
                        getattr(localedata, 'locale_identifiers'))
    locale_identifiers = list_identifiers()

    for i in locale_identifiers:
        if find(i) is not None:
            language_list.append(i)

    # NOTE(luisg): Babel>=1.0,<1.3 has a bug where some OpenStack supported
    # locales (e.g. 'zh_CN', and 'zh_TW') aren't supported even though they
    # are perfectly legitimate locales:
    #     https://github.com/mitsuhiko/babel/issues/37
    # In Babel 1.3 they fixed the bug and they support these locales, but
    # they are still not explicitly "listed" by locale_identifiers().
    # That is  why we add the locales here explicitly if necessary so that
    # they are listed as supported.
    aliases = {'zh': 'zh_CN',
               'zh_Hant_HK': 'zh_HK',
               'zh_Hant': 'zh_TW',
               'fil': 'tl_PH'}
    for (locale, alias) in six.iteritems(aliases):
        if locale in language_list and alias not in language_list:
            language_list.append(alias)

    _AVAILABLE_LANGUAGES[domain] = language_list
    return copy.copy(language_list)
