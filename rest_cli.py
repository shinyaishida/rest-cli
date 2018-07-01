from bindable_rest_cmd import BindableRestCmd as RestCmd
import argparse
import os
import sys

if __name__ == '__main__':
    DESCRIPTION = 'REST CLI'
    PROGRAM = os.path.basename(sys.argv[0])
    OPTIONS = {
        'url_root': {'metavar': 'URL', 'default': 'http://localhost',
                     'help': 'URL to connect'}
    }

    parser = argparse.ArgumentParser(prog=PROGRAM, description=DESCRIPTION)
    for option, option_params in OPTIONS.items():
        parser.add_argument(option, **option_params)
    args = parser.parse_args(sys.argv[1:])
    cmd = RestCmd(**vars(args))
    cmd.cmdloop()
