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
        for ref in refs:
            pushes.append(origin.push(':{0}'.format(ref.remote_head)))

        return pushes
