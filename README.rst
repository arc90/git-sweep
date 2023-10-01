=========
git-sweep
=========

📚 Overview
-----------

Feature branches are meant to be short-lived and merged into ``master`` once they are completed. However, after merging users often forget to delete these branches, and over time, forgotten branches can build up and create **a long and messy list of branches that are no longer needed**.

``git-sweep`` is a command-line tool that helps you clean up and **safely remove remote branches that have been merged into** ``master``.

For more information on Git branches, models such as `GitHub Flow`_ and Vincent Driessen's `git-flow`_, describe methods for using them.

.. contents:: **Table of Contents**

🔗 Dependencies
------------

* Git >= 1.7
* Python >= 2.6

🔧 Installation
------------

To install ``git-sweep``, ensure Python has been installed, then open the command-line and run the following prompt:

::

    pip install git-sweep || easy_install git-sweep


🚀 Getting Started
-------------------

To use ``git-sweep``, first change the current working directory to the Git repository that will be cleaned:

::

    $ cd myrepo

Preview Command
~~~~~~~~~~~~~~~

The ``preview`` command allows you to preview what ``git-sweep`` would delete with the ``cleanup`` command. It tells ``git-sweep`` to detect all branches merged into the master branch and print them as a list. It does not alter the repository:

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

Cleanup Command
~~~~~~~~~~~~~~~

The ``cleanup`` command will tell ``git-sweep`` to delete all remote branches merged with ``master``. Before deleting, it will print the branches it will delete and ask for your confirmation. Upon approval ``git-sweep`` will delete the branches from the remote repository:

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

⚙️ Options
-------

Skipping Branches
~~~~~~~~~~~~~~~~~

The ``--skip`` option allows you to skip specified branches when using the ``preview`` or ``cleanup`` commands.

::

    $ git-sweep preview --skip=develop
    Fetching from the remote
    These branches have been merged into master:

      important-upgrade
      upgrade-libs
      derp-removal

    To delete them, run again with `git-sweep cleanup --skip=develop`

Deleting Local Branches
~~~~~~~~~~~~~~~~~~~~~~~

To delete local branches, use the ``--origin=local`` option:

:: 

    $ cd myrepo
    $ git remote add local $(pwd)
    $ git-sweep cleanup --origin=local

Skipping Git Fetch
~~~~~~~~~~~~~~~~~~

By default, ``git-sweep`` will first fetch from the remote repository when using ``preview`` or ``cleanup``. You can skip this step by using the ``--nofetch`` option:

::

    $ git-sweep preview --nofetch
    These branches have been merged into master:

      branch1

    To delete them, run again with `git-sweep cleanup --nofetch`

Forced Delete
~~~~~~~~~~~~~

By default, before ``git-sweep`` begins deleting branches, it will ask for your confirmation:

::

    Delete these branches? (y/n)

You can use the ``--force`` option to bypass this and start deleting immediately.

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
    
Renaming Branches
~~~~~~~~~~~~~~~~~

Using the following options, you can give the remote and master branches different names.

::

    $ git-sweep preview --master=develop --origin=github
    ...

🛠️ Development
-----------

If you want to hack on this with us, fork the project and create a pull request in the ``develop`` branch when you are finished.

``git-sweep`` uses `git-flow`_ for development and release cycles. To run the tests, bootstrap Buildout and run this command:

::

    $ git clone http://github.com/arc90/git-sweep.git
    $ cd git-sweep
    $ python2.7 bootstrap.py
    ...
    $ ./bin/buildout
    ...
    $ ./bin/test

We also use Tox_. Run the tests for Python 2.6 and 2.7 using the following command:

::

    $ ./bin/tox

📃 License
-------

* Just a friendly neighborhood MIT license.

.. _GitHub Flow: http://scottchacon.com/2011/08/31/github-flow.html
.. _git-flow: http://nvie.com/posts/a-successful-git-branching-model/
.. _Tox: http://pypi.python.org/pypi/tox
