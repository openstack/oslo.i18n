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
"""Test fixtures for working with oslo.i18n.

"""

import fixtures
import six

from oslo.i18n import _message


class Translation(fixtures.Fixture):
    """Fixture for managing translatable strings.

    This class provides methods for creating translatable strings
    using both lazy translation and immediate translation. It can be
    used to generate the different types of messages returned from
    oslo.i18n to test code that may need to know about the type to
    handle them differently (for example, error handling in WSGI apps,
    or logging).

    Use this class to generate messages instead of toggling the global
    lazy flag and using the regular translation factory.

    """

    def __init__(self, domain='test-domain'):
        """Initialize the fixture.

        :param domain: The translation domain. This is not expected to
                       coincide with an actual set of message
                       catalogs, but it can.
        :type domain: str
        """
        self.domain = domain

    def lazy(self, msg):
        """Return a lazily translated message.

        :param msg: Input message string. May optionally include
                    positional or named string interpolation markers.
        :type msg: str or unicode

        """
        return _message.Message(msg, domain=self.domain)

    def immediate(self, msg):
        """Return a string as though it had been translated immediately.

        :param msg: Input message string. May optionally include
                    positional or named string interpolation markers.
        :type msg: str or unicode

        """
        return six.text_type(msg)
