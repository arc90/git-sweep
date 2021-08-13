from collections import namedtuple

from git import GitCommandError

from .base import BaseOperation


class Deleter(BaseOperation):

    """
    Removes remote branches from the remote.

    """
    def remove_remote_refs(self, refs):
        """
        Removes the remote refs from the remote.

        ``refs`` should be a lit of ``git.RemoteRefs`` objects.
        """
        origin = self._origin

        pushes = []
        errors = []
        for ref in refs:
            try:
                pushes.append(origin.push(':{0}'.format(ref.remote_head)))
            except GitCommandError:
                errors.append(ref.remote_head)

        RemoveResults = namedtuple('RemoveResults', 'pushes errors')
        return RemoveResults(pushes, errors)
