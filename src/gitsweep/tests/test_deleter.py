from gitsweep.tests.testcases import (GitSweepTestCase, InspectorTestCase,
    DeleterTestCase)


class TestDeleter(GitSweepTestCase, InspectorTestCase, DeleterTestCase):

    """
    Can delete remote refs from a remote.

    """
    def setUp(self):
        super(TestDeleter, self).setUp()

        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

    def test_will_delete_merged_from_clone(self):
        """
        Given a list of refs, will delete them from cloned repo.

        This test looks at our cloned repository, the one which is setup to
        track the remote and makes sure that the changes occur on it as
        expected.
        """
        clone = self.remote.remotes[0]

        # Grab all the remote branches
        before = [i.remote_head for i in clone.refs]
        # We should have 5 branches plus HEAD and master
        self.assertEqual(7, len(before))

        # Delete from the remote through the clone
        pushes = self.deleter.remove_remote_refs(
            self.merged_refs(refobjs=True))

        # Make sure it removed the expected number
        self.assertEqual(5, len(pushes))

        # Grab all the remote branches again
        after = [i.remote_head for i in clone.refs]
        after.sort()

        # We should be down to 2, HEAD and master
        self.assertEqual(['HEAD', 'master'], after)

    def test_will_delete_merged_on_remote(self):
        """
        With the list of refs, will delete these from the remote.

        This test makes assertion against the remote, not the clone repository.
        We are testing to see if the interactions in the cloned repo are pushed
        through to the remote.

        Note that accessing the repository directly does not include the
        symbolic reference of HEAD.
        """
        remote = self.repo

        # Get a list of branches on this remote
        before = [i.name for i in remote.refs]
        # Should be 5 branches + master
        self.assertEqual(6, len(before))

        # Delete through the clone which pushes to this remote
        pushes = self.deleter.remove_remote_refs(
            self.merged_refs(refobjs=True))

        # Make sure it removed the expected number
        self.assertEqual(5, len(pushes))

        # Grab again
        after = [i.name for i in remote.refs]
        # Should be down to just master
        self.assertEqual(['master'], after)
