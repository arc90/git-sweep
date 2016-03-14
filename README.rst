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

Using ``git-sweep`` you can **safely remove remote branches that have been
merged into master**.

To install it run:

::

    pip install git-sweep || easy_install git-sweep

Try it for yourself (safely)
----------------------------

To see a list of branches that git-sweep detects are merged into your master branch:

You need to have your Git repository as your current working directory.

::

    $ cd myrepo

The ``preview`` command doesn't make any changes to your repo.

::

    $ git-sweep preview
    Fetching from the remote
    These branches have been merged into master:

      branch1
      branch2
      branch3
      branch4
      branch5

    To delete them, run again with `git-sweep cleanup`

If you are happy with the list, you can run the command that deletes these
branches from the remote, ``cleanup``:

::

    $ git-sweep cleanup
    Fetching from the remote
    These branches have been merged into master:

      branch1
      branch2
      branch3
      branch4
      branch5

    Delete these branches? (y/n) y
      deleting branch1 (done)
      deleting branch2 (done)
      deleting branch3 (done)
      deleting branch4 (done)
      deleting branch5 (done)

    All done!

    Tell everyone to run `git fetch --prune` to sync with this remote.
    (you don't have to, yours is synced)

*Note: this can take a little time, it's talking over the tubes to the remote.*

You can also give it a different name for your remote and master branches.

::

    $ git-sweep preview --master=develop --origin=github
    ...

Tell it to skip the ``git fetch`` that it does by default.

::

    $ git-sweep preview --nofetch
    These branches have been merged into master:

      branch1

    To delete them, run again with `git-sweep cleanup --nofetch`

Make it skip certain branches.

::

    $ git-sweep preview --skip=develop
    Fetching from the remote
    These branches have been merged into master:

      important-upgrade
      upgrade-libs
      derp-removal

    To delete them, run again with `git-sweep cleanup --skip=develop`

Once git-sweep finds the branches, you'll be asked to confirm that you wish to
delete them.

::

    Delete these branches? (y/n)

You can use the ``--force`` option to bypass this and start deleting
immediately.

::

    $ git-sweep cleanup --skip=develop --force
    Fetching from the remote
    These branches have been merged into master:

      important-upgrade
      upgrade-libs
      derp-removal

      deleting important-upgrade (done)
      deleting upgrade-libs (done)
      deleting derp-removal (done)

    All done!

    Tell everyone to run `git fetch --prune` to sync with this remote.
    (you don't have to, yours is synced)
    
    
Deleting local branches
-----------

You can also clean up local branches by using simple hack:

:: 

    $ cd myrepo
    $ git remote add local $(pwd)
    $ git-sweep cleanup --origin=local
    

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

We also use Tox_. It will run the tests for Python 2.6 and 2.7.

::

    $ ./bin/tox

Requirements
------------

* Git >= 1.7
* Python >= 2.6

License
-------

Friendly neighborhood MIT license.

.. _GitHub Flow: http://scottchacon.com/2011/08/31/github-flow.html
.. _git-flow: http://nvie.com/posts/a-successful-git-branching-model/
.. _Tox: http://pypi.python.org/pypi/tox
