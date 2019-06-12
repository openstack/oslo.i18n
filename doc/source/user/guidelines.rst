=================================
 Guidelines for Use in OpenStack
=================================

The OpenStack I18N team has a limited capacity to translate messages,
so we want to make their work as effective as possible by identifying
the most useful text for them to translate.  All text messages *the
user sees* via exceptions or API calls should be marked for
translation. However, some exceptions are used internally to signal
error conditions between modules and are not intended to be presented
to the user.  Those do not need to be translated.  Neither do log
messages, as explained below.

.. seealso::

   * :ref:`usage`
   * :ref:`api`

Gettext Contextual Form and Plural Form
=======================================

Sometimes under different contexts, the same word should be
translated into different phrases using
:py:attr:`TranslatorFactory.contextual_form <oslo_i18n.TranslatorFactory.contextual_form>`.

And recommend the following code to use contextual form::

  # The contextual translation function using the name "_C"
  _C = _translators.contextual_form

  ...
  msg = _C('context', 'string')

In some languages, sometimes the translated strings are different
with different item counts using
:py:attr:`TranslatorFactory.plural_form <oslo_i18n.TranslatorFactory.plural_form>`

And recommend the following code to use plural form::

  # The plural translation function using the name "_P"
  _P = _translators.plural_form

  ...
  msg = _P('single', 'plural', count)

The contextual form and plural form are used only when needed.
By default, the translation should use the ``_()``.

.. note::
   These two functions were only available in oslo.i18n >= 2.1.0.

Log Translation
===============

.. note::

   Starting with the Pike series, OpenStack no longer supports log
   translation. It is not necessary to add translation instructions to
   new code, and the instructions can be removed from old code.  The
   following documentation is retained to help developers understand
   existing usage and how to remove it.

   Support was `dropped
   <http://lists.openstack.org/pipermail/openstack-dev/2017-March/114191.html>`_
   primarily based on `feedback from operators
   <http://lists.openstack.org/pipermail/openstack-operators/2017-March/012953.html>`_
   that they were not only not needed but also undesirable, because they
   fragmented the set of web pages providing helpful information about
   any particular log message, thereby reducing the chances of finding
   those web pages by doing a web search for the message.  Refer to
   the email thread `understanding log domain change
   <http://lists.openstack.org/pipermail/openstack-dev/2017-March/thread.html#113365>`_
   on the openstack-dev mailing list for more details.

OpenStack previously supported translating some log levels using
separate message catalogs, and so has separate marker functions. These
well-known names were used by the build system jobs that extracted the
messages from the source code and passed them to the translation tool.

========== ==========
 Level      Function
========== ==========
 INFO       ``_LI()``
 WARNING    ``_LW()``
 ERROR      ``_LE()``
 CRITICAL   ``_LC()``
========== ==========

.. note::
   Debug level log messages were never translated.


Using a Marker Function
=======================

The marker functions are used to mark the translatable strings in the
code.  The strings are extracted into catalogs using a tool that
performs source inspection to look for these specific markers, so the
function argument must just be a string.

For example: **do not do this**::

  # WRONG
  msg = _(variable_containing_msg)

Instead, use this style::

  # RIGHT
  msg = _('My message.')


Choosing a Marker Function
==========================

The purpose of the different marker functions is to separate the
translatable messages into different catalogs, which the translation
teams can prioritize translating. It is important to choose the right
marker function, to ensure that strings the user sees will be
translated and to help the translation team manage their work load.

Everything marked with ``_()`` will be translated. Prioritizing the
catalogs created from strings marked with the log marker functions is
up to the individual translation teams and their users, but it is
expected that they will work on critical and error messages before
warning or info.

``_()`` is preferred for any user facing message, even if it is also
going to a log file.  This ensures that the translated version of the
message will be available to the user.

The log marker functions (``_LI()``, ``_LW()``, ``_LE()``, and
``_LC()``) should no longer be used, and existing usages should be
removed.  Anytime that the message is passed outside of the current
context (for example as part of an exception) the ``_()`` marker
function must be used instead.

A common pattern used to be to define a single message object and use
it more than once, for the log call and the exception.  In that case,
``_()`` had to be used because the message was going to appear in an
exception that may be presented to the user.

However, now that log messages are no longer translated, it is
unfortunately necessary to use two separate strings: a plain one for
the log message, and a translatable one for the exception.

For example, **do not do this**::

  # WRONG
  msg = _('There was an error.')
  LOG.error(msg)
  raise LocalExceptionClass(msg)

or this::

  # EVEN MORE WRONG
  msg = _LE('There was an error.')
  LOG.error(msg)
  raise LocalExceptionClass(msg)

Instead, use this style::

  # RIGHT
  LOG.error('There was an error.')
  raise LocalExceptionClass(_('An error occurred.'))


Adding Variables to Translated Messages
=======================================

Translated messages should not be combined with other literal strings
to create partially translated messages.  For example, **do not do
this**::

  # WRONG
  raise ValueError(_('some message') + ': variable=%s' % variable)

Instead, use this style::

  # RIGHT
  raise ValueError(_('some message: variable=%s') % variable)

Including the variable reference inside the translated message allows
the translator to take into account grammar rules, differences in
left-right vs. right-left rendering, and other factors to make the
translated message more useful to the end user.

Any message with more than one variable should use named interpolation
instead of positional, to allow translators to move the variables
around in the string to account for differences in grammar and writing
direction.

For example, **do not do this**::

  # WRONG
  raise ValueError(_('some message: v1=%s v2=%s') % (v1, v2))

Instead, use this style::

  # RIGHT
  raise ValueError(_('some message: v1=%(v1)s v2=%(v2)s') % {'v1': v1, 'v2': v2})
