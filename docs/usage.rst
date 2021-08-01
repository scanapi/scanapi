..  documentation: usage

    Copyright ©  2019 Camila Maia <cmaiacd@gmail.com>

    ## LICENSE_SHORT ##
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#############################################################################
Using `ScanAPI`
#############################################################################

********
Overview
********

**TODO**

This project is based on the :gh:`Springerle/py-generic-project` cookiecutter.
Distribution packages are versioned according to :pep:`440`.


*****************
Command Line Tool
*****************

The :command:`scanapi` tool uses a sub-command scheme, like known from `git`.

Add :ref:`global options <global-opts>` directly after the :command:`scanapi` command name, and other options
after their sub-command. To get detailed help for a specific sub-command,
use a local :option:`--help` option as in ``scanapi help --help``.

.. warning::

    .. rubric:: Status: ALPHA

    Not all of these options and commands are implemented yet!


.. _cmd-help:

The `help` Command
==================

Call ``scanapi help`` to check if your installation basically works.
The output shows version information and install locations.
It also lists the paths where configuration files are read from,
see :option:`--config` and :envvar:`SCANAPI_CONFIG` on how to provide a custom path.



.. _global-opts:

Global Command Line Options
===========================

Global options must be used *before* any sub-command, e.g. ``scanapi -c :/dev/null help``.

.. option:: --version

    Show the version and install location, then exit.

.. option:: --license

    Show the license text and exit.

.. option:: -q, --quiet

    Be quiet and only show error messages.

.. option:: -v, --verbose

    Create extra verbose output.

.. option:: -c, --config FILE

    Load given configuration file(s). This overwrites the default lookup path for configuration files.

    You can provide this option multiple times, and also provide PATH-like lists separated by a colon.
    An empty path component ``-c ''`` restores the default lookup path, at the place you used it.

    See also :envvar:`SCANAPI_CONFIG` on how to use the environment for this.

.. option:: -h, --help

    Show a usage message and exit.


.. _env-vars:

Environment Variables
=====================

Certain environment variables can be used to customise the behaviour
of the application.

.. envvar:: SCANAPI_CONFIG

   A PATH-like list of *additional* config files, read after the default ones.

   See also :option:`--config` for ad-hoc changes on the command line.
