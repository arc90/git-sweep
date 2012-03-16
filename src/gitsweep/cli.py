import sys
from os import getcwd
from argparse import ArgumentParser

from git import Repo, InvalidGitRepositoryError

from gitsweep.inspector import Inspector
from gitsweep.deleter import Deleter


class CommandLine(object):

    """
    Main interface to the command-line for running git-sweep.

    """
    parser = ArgumentParser(
        description='Clean up your Git repository remote branches',
        prog='git-sweep')

    _sub_parsers = parser.add_subparsers(title='action',
        description='Preview changes or perform clean up')

    _origin_kwargs = {
        'help': 'The name of the remote you wish to clean up',
        'dest': 'origin',
        'default': 'origin'}

    _master_kwargs = {
        'help': 'The name of what you consider the master branch',
        'dest': 'master',
        'default': 'master'}

    _no_fetch_kwargs = {
        'help': 'Do not fetch from the remote',
        'dest': 'fetch',
        'action': 'store_false',
        'default': True}

    _preview = _sub_parsers.add_parser('preview',
        help='Preview the branches that will be deleted')
    _preview.add_argument('--origin', **_origin_kwargs)
    _preview.add_argument('--master', **_master_kwargs)
    _preview.add_argument('--nofetch', **_no_fetch_kwargs)
    _preview.set_defaults(action='preview')

    _cleanup = _sub_parsers.add_parser('cleanup',
        help='Delete merged branches from the remote')
    _cleanup.add_argument('--origin', **_origin_kwargs)
    _cleanup.add_argument('--master', **_master_kwargs)
    _cleanup.add_argument('--nofetch', **_no_fetch_kwargs)
    _cleanup.set_defaults(action='cleanup')

    def __init__(self, args):
        self.args = args[1:]

    def run(self):
        """
        Runs git-sweep.
        """
        try:
            self._sweep()

            sys.exit(0)
        except InvalidGitRepositoryError:
            sys.stdout.write('This is not a Git repository\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n')

        sys.exit(1)

    def _sweep(self):
        """
        Runs git-sweep.
        """
        args = self.parser.parse_args(self.args)

        dry_run = True if args.action == 'preview' else False
        fetch = args.fetch

        # Is this a Git repository?
        repo = Repo(getcwd())

        remote_name = args.origin

        # Fetch from the remote so that we have the latest commits
        if fetch:
            for remote in repo.remotes:
                if remote.name == remote_name:
                    sys.stdout.write('Fetching from the remote\n')
                    remote.fetch()

        master_branch = args.master

        # Find branches that could be merged
        inspector = Inspector(repo, remote_name=remote_name,
            master_branch=master_branch)
        ok_to_delete = inspector.merged_refs()

        if ok_to_delete:
            sys.stdout.write(
                'These branches have been merged into {}:\n\n'.format(
                    master_branch))
        else:
            sys.stdout.write('No remote branches are available for '
                'cleaning up\n')

        for ref in ok_to_delete:
            sys.stdout.write('  {}\n'.format(ref.remote_head))

        if not dry_run:
            deleter = Deleter(repo, remote_name=remote_name,
                master_branch=master_branch)

            sys.stdout.write('\nDelete these branches? (y/n) ')
            answer = raw_input()
            if answer.lower().startswith('y'):
                sys.stdout.write('\n')
                for ref in ok_to_delete:
                    sys.stdout.write('  deleting {}'.format(ref.remote_head))
                    deleter.remove_remote_refs([ref])
                    sys.stdout.write(' (done)\n')

                sys.stdout.write('\nAll done!\n')
                sys.stdout.write('\nTell everyone to run `git fetch --prune` '
                    'to sync with this remote.\n')
                sys.stdout.write('(you don\'t have to, your\'s is synced)')
            else:
                sys.stdout.write('\nOK, aborting.')
        elif ok_to_delete:
            sys.stdout.write(
                '\nTo delete them, run again with `git-sweep cleanup`')
