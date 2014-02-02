Python for Nerds
================

This document contains notes for people who already know a thing or two about
programming. It's not meant as a Python tutorial.

It contains Python Idioms/caveats you might find useful if coming from another language.

Idioms
------

Know the basic data types
~~~~~~~~~~~~~~~~~~~~~~~~~

* The **big one** between Python2 and Python3: String literals::

    # ------ Python 2 --------------------------
    x = 'text'  # x is a chain of bytes, which - if all contained
                # bytes are ASCII characters - can be considered
                # for all intents and purposes a string. But you
                # should always know the proper codec to convert
                # this to/from actual text!
    x = u'text'  # x is now a unicode object, or in other words,
                 # contains real text. This is usually what you
                 # want! ALWAYS use the 'u' prefix in Python2 when
                 # you are talking "human text".
    x = b'text'  # equivalent to x = 'text'

    # ------ Python 3 --------------------------
    x = 'text'  # a unicode object (see above for details)
    x = u'text' # equivalent to x = 'text'
    x = b'text' # a chain of bytes.

* A :py:class:`list` is a *mutable* ordered collection. Similar to an "array"
  elsewhere.  (Don't bother with :py:mod:`array` unless you *reaaaaaaly* need
  to!)
* A :py:class:`tuple` is an *immutable* ordered collection (thus also
  hashable)! Check out the new :py:func:`collections.namedtuple` also for code
  (and error/debugging) readability.
* A :py:class:`dict` is similar to a hashtable (mutable, unhashable).
* A :py:class:`set` is a *mutable* unordered collection which contains only
  unique elements (elements must be hashable). Supports math ops like
  :py:meth:`~set.union`, :py:meth:`~set.intersection`, ...

All the gory details are at: http://docs.python.org/3.3/library/stdtypes.html


``in`` is your friend
~~~~~~~~~~~~~~~~~~~~~

It checks for:

* if substring is in a string (no need to search for an index, or use regexes)
* if a key is contained in a dictionary
* if a value is in a list
* everything which implements :py:meth:`object.__contains__` (for example
  (py3): ``ip_address('1.2.3.4') in ip_network('1.2.3.0/24')``)


``for`` can loop over many things
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* items in a list/tuple (duh): ``for item in mylist``
* keys in a dictionary: ``for key in mydict``
* characters in a string/bytestream: ``for char in mystring``
* lines in a file: ``for line in file``
* generators
* everything which implements :py:meth:`iterator.__iter__`


Joining a list of string to form a new string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    print '\n'.join(['line1', 'line2', 'line3'])


Getting a key from a dictionary with default value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simply do::

    value = data.get('key', 'mydefault')

instead of::

    try:
        value = data['key']
    except KeyError:
        value = 'mydefault'


The ternary operator
~~~~~~~~~~~~~~~~~~~~

Two options::

    val = 10 if check else 20  # considered more "pythonic"

or::

    val = check and 10 or 20  # same token ordering as the classic ternary.
                              # Essentially a hack on the fact that ``and`` and
                              # ``or`` return values in python, and their
                              # precedence.

Variable Unpacking
~~~~~~~~~~~~~~~~~~

.. warning::

  This might raise a :py:class:`ValueError` if you try to unpack the wrong
  number of arguments. Additionally, if you store the result in just one
  variable, you will get a tuple instead!

::

    def func_returns_tuple_with_two_values():
      return (1, 2)

    val_1, val_2 = func_returns_tuple_with_two_values()


Checking for "falsyness"
~~~~~~~~~~~~~~~~~~~~~~~~

In Python, not only ``False`` is considered as ``False`` in a boolean context
(typically in an ``if``-statement). This includes ``None``, the empty string
and empty lists. You should *only* check for these values explicitly if you
really need to::

    if not my_string_value:
        print("var `my_string_value` is empty")

    if not my_list:
        print("The list `my_list` is empty")



Sorting Collections
~~~~~~~~~~~~~~~~~~~

::

    # Leaves the original list intact, returns a new, sorted list
    new_list = sorted(old_list)

    # Mutates the original list
    list.sort()


Advanced sorting
~~~~~~~~~~~~~~~~

Pass in a function which takes one element, and returns the value to sort by::

    def my_key_func(element):
        return element.sortable_argument

    new_list = sorted(old_list, key=my_key_func)


Caveats
-------

Mutable objects as default arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Careful with this::

    def myfunc(thelist=[]):
        print thelist

... or this::

    class MyObj(object):
      pass

    def myfunc(data=MyObj()):
      print data.values

As Python is an interpreted language, these values will be instantiated at the
time the function is *defined*! **Not** when it's executed! This means that
these value will effectively behave a bit like singletons or static values!
This can be useful at times, but might bite you if you're not careful. Instead,
you usually want to use this as alternative::

    def myfunc(data=None):
      if not data:
        data = MyObj()  # or: data = []
