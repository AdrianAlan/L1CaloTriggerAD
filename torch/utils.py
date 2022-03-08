import argparse
import os


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt

    def reset(self):
        self.count = 0
        self.average = 0
        self.sum = 0

    def update(self, value, num=1):
        self.count += num
        self.sum += value * num
        self.average = self.sum / self.count

    def __str__(self):
        fmtstr = '{average' + self.fmt + '} ({name})'
        return fmtstr.format(**self.__dict__)


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


def to_numpy(t):
    return t.detach().cpu().numpy() if t.requires_grad else t.cpu().numpy()
