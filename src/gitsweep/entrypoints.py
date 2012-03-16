def main():
    """
    Command-line interface.
    """
    import sys

    from gitsweep.cli import CommandLine

    CommandLine(sys.argv).run()


def test():
    """
    Run git-sweep's test suite.
    """
    import nose

    import sys

    nose.main(argv=['nose'] + sys.argv[1:])
