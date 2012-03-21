from gitsweep.tests.testcases import GitSweepTestCase, InspectorTestCase


class TestInspector(GitSweepTestCase, InspectorTestCase):

    """
    Inspector can find merged branches and present them for cleaning.

    """
    def test_no_branches(self):
        """
        If only the master branch is present, nothing to clean.
        """
        self.assertEqual([], self.inspector.merged_refs())

    def test_filtered_refs(self):
        """
        Will filter references and not return HEAD and master.
        """
        for i in range(1, 4):
            self.command('git checkout -b branch{0}'.format(i))
            self.command('git checkout master')

        refs = self.inspector._filtered_remotes(
            self.inspector.repo.remotes[0])

        self.assertEqual(['branch1', 'branch2', 'branch3'],
            [i.remote_head for i in refs])

    def test_one_branch_no_commits(self):
        """
        There is one branch on the remote that is the same as master.
        """
        self.command('git checkout -b branch1')
        self.command('git checkout master')

        # Since this is the same as master, it should show up as merged
        self.assertEqual(['branch1'], self.merged_refs())

    def test_one_branch_one_commit(self):
        """
        A commit has been made in the branch so it's not safe to remove.
        """
        self.command('git checkout -b branch1')

        self.make_commit()

        self.command('git checkout master')

        # Since there is a commit in branch1, it's not safe to remove it
        self.assertEqual([], self.merged_refs())

    def test_one_merged_branch(self):
        """
        If a branch has been merged, it's safe to delete it.
        """
        self.command('git checkout -b branch1')

        self.make_commit()

        self.command('git checkout master')

        self.command('git merge branch1')

        self.assertEqual(['branch1'], self.merged_refs())

    def test_commit_in_master(self):
        """
        Commits in master not in the branch do not block it for deletion.
        """
        self.command('git checkout -b branch1')

        self.make_commit()

        self.command('git checkout master')

        self.make_commit()

        self.command('git merge branch1')

        self.assertEqual(['branch1'], self.merged_refs())

    def test_large_set_of_changes(self):
        r"""
        A long list of changes is properly marked for deletion.

        The branch history for this will look like this:

        ::

            |\
            | * 08d07e1 Adding 4e510716
            * | 056abb2 Adding a0dfc9fb
            |/
            *   9d77626 Merge branch 'branch4'
            |\
            | * 956b3f9 Adding e16ec279
            * | d11315e Adding 9571d55d
            |/
            *   f100932 Merge branch 'branch3'
            |\
            | * c641899 Adding 9b33164f
            * | 17c1e35 Adding b56c43be
            |/
            *   c83c8d3 Merge branch 'branch2'
            |\
            | * bead4e5 Adding 31a13fa4
            * | 5a88ec3 Adding b6a45f21
            |/
            *   f34643d Merge branch 'branch1'
            |\
            | * 8e110c4 Adding 11948eb5
            * | 4c94394 Adding db29f4aa
            |/
        """
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        self.assertEqual(
            ['branch1', 'branch2', 'branch3', 'branch4', 'branch5'],
            self.merged_refs())
