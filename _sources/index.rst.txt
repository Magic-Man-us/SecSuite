SecSuite Documentation
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/modules
    security

Welcome to SecSuite
-------------------

SecSuite is a modern Python package built with best practices, including:

* Type hints with mypy
* Linting and formatting with Ruff
* Testing with pytest and coverage
* Documentation with Sphinx

Installation
------------

Create the development environment with uv and install dependencies::

    uv sync --all-extras

Quick Start
-----------

Here's a simple example::

    from secsuite import ExampleClass, example

    # Use the example class
    obj = ExampleClass(name="demo", value=42, tags=["python", "example"])
    result = obj.process()
    print(result)

    # Use the example function
    items = example(["hello", "world"])
    print(items)  # ['HELLO', 'WORLD']

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
