import argparse
import os


class IsReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                    '{0} is not a valid path'.format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                    '{0} is not a readable directory'.format(prospective_dir))


class IsValidFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_file = values
        if not os.path.exists(prospective_file):
            raise argparse.ArgumentTypeError(
                    '{0} is not a valid file'.format(prospective_file))
        else:
            setattr(namespace, self.dest, prospective_file)


def absoluteFilePaths(directory, extension='root'):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith(extension) and f.startswith('L1Ntuple'):
                yield os.path.abspath(os.path.join(dirpath, f))
