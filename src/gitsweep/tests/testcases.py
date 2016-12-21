import sys
from os import chdir, getcwd
from os.path import join, basename
from tempfile import mkdtemp
from unittest import TestCase
from uuid import uuid4 as uuid
from shutil import rmtree
from shlex import split
from contextlib import contextmanager
from textwrap import dedent

from mock import patch
from git import Repo
from git.cmd import Git

from gitsweep.inspector import Inspector
from gitsweep.deleter import Deleter
from gitsweep.cli import CommandLine


@contextmanager
def cwd_bounce(dir):
    """
    Temporarily changes to a directory and changes back in the end.

    Where ``dir`` is the directory you wish to change to. When the context
    manager exits it will change back to the original working directory.

    Context manager will yield the original working directory and make that
    available to the context manager's assignment target.
    """
    original_dir = getcwd()

    try:
        chdir(dir)

        yield original_dir
    finally:
        chdir(original_dir)


class GitSweepTestCase(TestCase):

    """
    Sets up a Git repository and provides some command to manipulate it.

    """
    def setUp(self):
        """
        Sets up the Git repository for testing.

        The following will be available after :py:method`setUp()` runs.

        self.repodir
            The absolute filename of the Git repository

        self.repo
            A ``git.Repo`` object for self.repodir

        This will create the root commit in the test repository automaticall.
        """
        super(GitSweepTestCase, self).setUp()

        repodir = mkdtemp()

        self.repodir = repodir
        self.repo = Repo.init(repodir)

        rootcommit_filename = join(repodir, 'rootcommit')

        with open(rootcommit_filename, 'w') as fh:
            fh.write('')

        self.repo.index.add([basename(rootcommit_filename)])
        self.repo.index.commit('Root commit')

        # Cache the remote per test
        self._remote = None

        # Keep track of cloned repositories that track self.repo
        self._clone_dirs = []

    def tearDown(self):
        """
        Remove any created repositories.
        """
        rmtree(self.repodir)

        for clone in self._clone_dirs:
            rmtree(clone)

    def assertResults(self, expected, actual):
        """
        Assert that output matches expected argument.
        """
        expected = dedent(expected).strip()

        actual = actual.strip()

        self.assertEqual(expected, actual)

    def command(self, command):
        """
        Runs the Git command in self.repo
        """
        args = split(command)

        cmd = Git(self.repodir)

        cmd.execute(args)

    @property
    def remote(self):
        """
        Clones the test case's repository and tracks it as a remote.

        Returns a ``git.Repo`` object.
        """
        if not self._remote:
            clonedir = mkdtemp()
            self._clone_dirs.append(clonedir)

            self._remote = Repo.clone(self.repo, clonedir)

        # Update in case the remote has changed
        self._remote.remotes[0].pull()
        return self._remote

    def graph(self):
        """
        Prints a graph of the git log.

        This is used for testing and debugging only.
        """
        sys.stdout.write(Git(self.repodir).execute(
            ['git', 'log', '--graph', '--oneline']))

    def make_commit(self):
        """
        Makes a random commit in the current branch.
        """
        fragment = uuid().hex[:8]
        filename = join(self.repodir, fragment)
        with open(filename, 'w') as fh:
            fh.write(uuid().hex)

        self.repo.index.add([basename(filename)])
        self.repo.index.commit('Adding {0}'.format(basename(filename)))


class InspectorTestCase(TestCase):

    """
    Creates an Inspector object for testing.

    """
    def setUp(self):
        super(InspectorTestCase, self).setUp()

        self._inspector = None

    @property
    def inspector(self):
        """
        Return and optionally create an Inspector from self.remote.
        """
        if not self._inspector:
            self._inspector = Inspector(self.remote)

        return self._inspector

    def merged_refs(self, refobjs=False):
        """
        Get a list of branch names from merged refs from self.inspector.

        By default, it returns a list of branch names. You can return the
        actual ``git.RemoteRef`` objects by passing ``refobjs=True``.
        """
        refs = self.inspector.merged_refs()

        if refobjs:
            return refs

        return [i.remote_head for i in refs]


class DeleterTestCase(TestCase):

    """
    Creates a Deleter object for testing.

    """
    def setUp(self):
        super(DeleterTestCase, self).setUp()

        self._deleter = None

    @property
    def deleter(self):
        """
        Return and optionally create a Deleter from self.remote.
        """
        if not self._deleter:
            self._deleter = Deleter(self.remote)

        return self._deleter


class CommandTestCase(GitSweepTestCase, InspectorTestCase, DeleterTestCase):

    """
    Used to test the command-line interface.

    """
    def setUp(self):
        super(CommandTestCase, self).setUp()

        self._commandline = None
        self._original_dir = getcwd()

        # Change the working directory to our clone
        chdir(self.remote.working_dir)

    def tearDown(self):
        """
        Change back to the original directory.
        """
        chdir(self._original_dir)

    @property
    def cli(self):
        """
        Return and optionally create a CommandLine object.
        """
        if not self._commandline:
            self._commandline = CommandLine([])

        return self._commandline

    def gscommand(self, command):
        """
        Runs the command with the given args.
        """
        exit_code = None
        args = split(command)

        self.cli.args = args[1:]

        with patch.object(sys, 'stdout'), patch.object(sys, 'stderr'):
            stdout = sys.stdout
            stderr = sys.stderr
            try:
                self.cli.run()
            except SystemExit as se:
                exit_code = se.code

        stdout = ''.join([i[0][0] for i in stdout.write.call_args_list])
        stderr = ''.join([i[0][0] for i in stderr.write.call_args_list])

        return (exit_code, stdout, stderr)
