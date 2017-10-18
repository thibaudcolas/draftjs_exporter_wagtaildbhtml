.. image:: https://img.shields.io/pypi/v/draftjs_exporter_wagtaildbhtml.svg
   :target: https://pypi.python.org/pypi/draftjs_exporter_wagtaildbhtml
.. image:: https://travis-ci.org/thibaudcolas/draftjs_exporter_wagtaildbhtml.svg?branch=master
   :target: https://travis-ci.org/thibaudcolas/draftjs_exporter_wagtaildbhtml
.. image:: https://coveralls.io/repos/github/thibaudcolas/draftjs_exporter_wagtaildbhtml/badge.svg?branch=master
   :target: https://coveralls.io/github/thibaudcolas/draftjs_exporter_wagtaildbhtml?branch=master

draftjs_exporter_wagtaildbhtml 🐍
=================================

    Convert the Facebook Draft.js editor’s raw ContentState to Wagtail's DB-HTML representation

Installation
~~~~~~~~~~~~

    Requirements: ``virtualenv``, ``pyenv``, ``twine``

.. code:: sh

    git clone git@github.com:thibaudcolas/draftjs_exporter_wagtaildbhtml.git
    cd draftjs_exporter_wagtaildbhtml/
    # Install the git hooks.
    ./.githooks/deploy
    # Install the Python environment.
    virtualenv .venv
    source ./.venv/bin/activate
    make init
    # Install required Python versions
    pyenv install --skip-existing 2.7.11
	pyenv install --skip-existing 3.4.4
	pyenv install --skip-existing 3.5.1
    # Make required Python versions available globally.
    pyenv global system 2.7.11 3.4.4 3.5.1

Commands
~~~~~~~~

.. code:: sh

    make help            # See what commands are available.
    make init            # Install dependencies and initialise for development.
    make lint            # Lint the project.
    make test            # Test the project.
    make test-watch      # Restarts the tests whenever a file changes.
    make test-coverage   # Run the tests while generating test coverage data.
    make test-ci         # Continuous integration test suite.
    make dev             # Restarts the example whenever a file changes.
    make clean-pyc       # Remove Python file artifacts.
    make publish         # Publishes a new version to pypi.

Debugging
~~~~~~~~~

*  Always run the tests. ``npm install -g nodemon``, then ``make test-watch``.
*  Use a debugger. ``pip install ipdb``, then ``import ipdb; ipdb.set_trace()``.
