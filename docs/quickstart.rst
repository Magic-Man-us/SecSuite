Quick Start
===========

Basic Usage
-----------

Here's how to get started with SecSuite:

Using ExampleClass
~~~~~~~~~~~~~~~~~~

The ``ExampleClass`` is a frozen dataclass that demonstrates best practices::

    from secsuite import ExampleClass

    # Create an instance
    obj = ExampleClass(name="demo", value=42)
    
    # Process the data
    result = obj.process()
    print(result)
    # Output: {'name': 'demo', 'value': 42, 'tag_count': 0}

With Tags
~~~~~~~~~

You can also include tags::

    obj = ExampleClass(
        name="tagged_example",
        value=100,
        tags=["python", "demo", "example"]
    )
    
    result = obj.process()
    print(result["tag_count"])  # Output: 3

Using the example Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``example`` function processes sequences of strings::

    from secsuite import example

    items = example(["hello", "world"])
    print(items)  # Output: ['HELLO', 'WORLD']

Writing to a File
~~~~~~~~~~~~~~~~~

You can optionally write the output to a file::

    from pathlib import Path
    from secsuite import example

    output_path = Path("output.txt")
    items = example(["hello", "world"], output_path=output_path)
    
    # The file now contains:
    # HELLO
    # WORLD

Error Handling
~~~~~~~~~~~~~~

The package includes proper validation::

    from secsuite import ExampleClass

    try:
        # This will raise ValueError
        obj = ExampleClass(name="", value=42)
    except ValueError as e:
        print(f"Error: {e}")

    try:
        # This will also raise ValueError
        obj = ExampleClass(name="test", value=-1)
    except ValueError as e:
        print(f"Error: {e}")

Next Steps
----------

* Check out the :doc:`api/modules` for detailed API documentation
* Read the source code for more examples
* Run the test suite to see comprehensive usage examples
