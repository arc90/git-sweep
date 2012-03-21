class MissingRemote(Exception):

    """
    Raise when a remote by name is not found.

    """
    pass


class MissingMasterBranch(Exception):

    """
    Raise when the "master" branch cannot be located.

    """
    pass


class BaseOperation(object):

    """
    Base class for all Git-related operations.

    """
    def __init__(self, repo, remote_name='origin', master_branch='master'):
        self.repo = repo
        self.remote_name = remote_name
        self.master_branch = master_branch

    def _filtered_remotes(self, origin, skip=[]):
        """
        Returns a list of remote refs, skipping ones you don't need.

        If ``skip`` is empty, it will default to ``['HEAD',
        self.master_branch]``.
        """
        if not skip:
            skip = ['HEAD', self.master_branch]

        refs = [i for i in origin.refs if not i.remote_head in skip]

        return refs

    def _master_ref(self, origin):
        """
        Finds the master ref object that matches master branch.
        """
        for ref in origin.refs:
            if ref.remote_head == self.master_branch:
                return ref

        raise MissingMasterBranch(
            'Could not find ref for {0}'.format(self.master_branch))

    @property
    def _origin(self):
        """
        Gets the remote that references origin by name self.origin_name.
        """
        origin = None

        for remote in self.repo.remotes:
            if remote.name == self.remote_name:
                origin = remote

        if not origin:
            raise MissingRemote('Could not find the remote named {0}'.format(
                self.remote_name))

        return origin
