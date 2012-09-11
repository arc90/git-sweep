import sys
from git import Git

from .base import BaseOperation


class Inspector(BaseOperation):

    """
    Used to introspect a Git repository.

    """
    def merged_refs(self, skip=[]):
        """
        Returns a list of remote refs that have been merged into the master
        branch.

        The "master" branch may have a different name than master. The value of
        ``self.master_name`` is used to determine what this name is.
        """
        origin = self._origin

        master = self._master_ref(origin)
        refs = self._filtered_remotes(
            origin, skip=['HEAD', self.master_branch] + skip)
        merged = []

        num_refs = len(refs)
        if self.verbose:
            sys.stdout.write("Found %d remote refs\n" % num_refs)

        for idx, ref in enumerate(refs):
            upstream = '{origin}/{master}'.format(
                origin=origin.name, master=master.remote_head)
            head = '{origin}/{branch}'.format(
                origin=origin.name, branch=ref.remote_head)
            if self.verbose:
                sys.stdout.write("Checking %s (%d/%d)...\n" % (head, idx + 1, num_refs))
            cmd = Git(self.repo.working_dir)
            # Drop to the git binary to do this, it's just easier to work with
            # at this level.
            (retcode, stdout, stderr) = cmd.execute(
                ['git', 'cherry', upstream, head],
                with_extended_output=True, with_exceptions=False)
            if retcode == 0 and not stdout:
                if self.verbose:
                    sys.stdout.write("...merged (ok to delete)\n")
                # This means there are no commits in the branch that are not
                # also in the master branch. This is ready to be deleted.
                merged.append(ref)
            else:
                if self.verbose:
                    sys.stdout.write("...not merged\n")

        return merged
