from git import Git

from .base import BaseOperation


class Inspector(BaseOperation):

    """
    Used to introspect a Git repository.

    """
    def merged_refs(self):
        """
        Returns a list of remote refs that have been merged into the master
        branch.

        The "master" branch may have a different name than master. The value of
        ``self.master_name`` is used to determine what this name is.
        """
        origin = self._origin

        master = self._master_ref(origin)
        refs = self._filtered_remotes(origin)
        merged = []

        for ref in refs:
            since_until = '{origin}/{master}..{origin}/{branch}'.format(
                origin=origin.name, master=master.remote_head,
                branch=ref.remote_head)
            cmd = Git(self.repo.working_dir)
            # Drop to the git binary to do this, it's just easier to work with
            # at this level.
            (retcode, _, _) = cmd.execute(
                ['git', 'log', '--exit-code', since_until],
                with_extended_output=True, with_exceptions=False)
            if retcode == 0:
                # This means there are no commits in the branch that are not
                # also in the master branch. This is ready to be deleted.
                merged.append(ref)

        return merged
