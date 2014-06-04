=======
 Usage
=======

Integration Module
==================

To use in a project, create a small integration module containing:

::

	from oslo.i18n import gettextutils

    _translators = gettextutils.TranslatorFactory(domain='myapp')

    # The primary translation function using the well-known name "_"
    _ = _translators.primary

    # Translators for log levels.
    #
    # The abbreviated names are meant to reflect the usual use of a short
    # name like '_'. The "L" is for "log" and the other letter comes from
    # the level.
    _LI = _translators.log_info
    _LW = _translators.log_warning
    _LE = _translators.log_error
    _LC = _translators.log_critical

Then, in your application code, use the appropriate marker function
for your case:

::

    from myapp.i18n import _, _LW

    # ...

    LOG.warn(_LW('warning message: %s'), var)

    # ...

    raise RuntimeError(_('exception message'))

Lazy Translation
================

Lazy translation delays converting a message string to the translated
form as long as possible, including possibly never if the message is
not logged or delivered to the user in some other way. It also
supports logging translated messages in multiple languages, by
configuring separate log handlers.

Lazy translation is implemented by returning a special object from the
translation function, instead of a unicode string. That special
message object supports some, but not all, string manipulation
APIs. For example, concatenation with addition is not supported, but
interpolation of variables is supported. Depending on how translated
strings are used in an application, these restrictions may mean that
lazy translation cannot be used, and so it is not enabled by default.

To enable lazy translation, call :func:`enable_lazy`.

::

    from oslo.i18n import gettextutils

    gettextutils.enable_lazy()
