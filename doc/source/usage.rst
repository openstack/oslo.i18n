=======
 Usage
=======

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
