git-sweep
=========

A command-line tool that helps you clean up Git branches that have been merged
into master.

One of the best features of Git is cheap branches. There are existing branching
models like `GitHub Flow`_ and Vincent Driessen's `git-flow`_ that describe
methods for using this feature.

The problem
-----------

Your ``master`` branch is typically where all your code lands. All features
branches are meant to be short-lived and merged into ``master`` once they are
completed.

As time marches on, you can build up **a long list of branches that are no
longer needed**. They've been merged into ``master``, what do we do with them
now?

The answer
----------

Using ``git-sweep`` you can *safely remove remote branches that have been
merged into master*.

Try it for yourself (safely)
----------------------------

::

    $ git-sweep preview

::

    $ git-sweep cleanup
    Are you sure you wish to delete 15 remote branches (y/n)?

::

    Instructions for having your team sync their branches

Development
-----------

git-sweep uses `git-flow`_ for development and release cylces. If you want to
hack on this with us, fork the project and put a pull request into the
``develop`` branch when you get done.

To run the tests, bootstrap Buildout and run this command:

::

    $ git clone http://github.com/arc90/git-sweep.git
    $ cd git-sweep
    $ python2.7 bootstrap.py
    ...
    $ ./bin/buildout
    ...
    $ ./bin/test

Requirements
------------

* Git >= 1.7
* Python >= 2.6

.. _GitHub Flow: http://scottchacon.com/2011/08/31/github-flow.html
.. _git-flow: http://nvie.com/posts/a-successful-git-branching-model/

License
-------

Friendly neighborhood MIT license:

.. include:: LICENSE.txt
