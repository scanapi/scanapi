..  documentation master file

    Copyright ©  2019 Camila Maia <cmaiacd@gmail.com>

    ## LICENSE_SHORT ##
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#############################################################################
Welcome to the “ScanAPI” manual!
#############################################################################

.. image:: _static/img/logo.png

Automated Integration Testing and Live Documentation for your API.


**********
Installing
**********

*ScanAPI* can be installed from PyPI
via ``pip install scanapi`` as usual,
see `releases <https://github.com/scanapi/scanapi/releases>`_
on GitHub for an overview of available versions – the project uses
`semantic versioning <http://semver.org/>`_ and follows
`PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_ conventions.
If no releases are available yet, install from source as described right below.

To get a bleeding-edge version from source, use these commands:

.. code-block:: shell

    repo="scanapi/scanapi"
    python3 -m venv ~/.local/venvs/scanapi && . $_/bin/activate
    python3 -m pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
    python3 -m pip install -e "git+https://github.com/$repo.git#egg=${repo#*/}"
    ln -nfs ../.local/venvs/scanapi/bin/scanapi ~/.local/bin

See the following section on how to create a full development environment.

To add bash completion, read the
`Click docs <http://click.pocoo.org/4/bashcomplete/#activation>`_
about it, or just follow these instructions:

.. code-block:: shell

    cmdname=scanapi
    mkdir -p ~/.bash_completion.d
    ( export _$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source ; \
      $cmdname >~/.bash_completion.d/$cmdname.sh )
    grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
        || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
    . "/etc/bash_completion"

After installation, continue with :doc:`usage`.


************
Contributing
************

To create a working directory for this project, call these commands:

.. code-block:: shell

    git clone "https://github.com/scanapi/scanapi.git"
    cd "scanapi"
    . .env --yes --develop
    invoke build --docs test check

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See :doc:`CONTRIBUTING` for more.


**********************
Documentation Contents
**********************

.. toctree::
    :maxdepth: 4

    usage
    cli-reference
    api-reference
    CONTRIBUTING
    LICENSE


**********
References
**********

Tools
=====

-  `Cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`_
-  `PyInvoke <http://www.pyinvoke.org/>`_
-  `pytest <http://pytest.org/latest/contents.html>`_
-  `tox <https://tox.readthedocs.io/en/latest/>`_
-  `Pylint <http://docs.pylint.org/>`_
-  `twine <https://github.com/pypa/twine#twine>`_
-  `bpython <http://docs.bpython-interpreter.org/>`_
-  `yolk3k <https://github.com/myint/yolk#yolk>`_

Packages
========

-  `Rituals <https://jhermann.github.io/rituals>`_
-  `Click <http://click.pocoo.org/>`_


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
