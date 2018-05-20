from rest_cmd import RestCmd
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='rest_cli.py', description='REST CLI')
    parser.add_argument('url_root', metavar='URL', default='http://localhost', help='URL to connect')
    args = parser.parse_args(sys.argv[1:])
    cmd = RestCmd(**vars(args))
    cmd.cmdloop()
