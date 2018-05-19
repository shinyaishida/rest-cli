from rest_cmd import RestCmd
import argparse
import sys

parser = argparse.ArgumentParser(prog='rest_cli.py', description='REST CLI')
parser.add_argument('url', default='http://localhost', help='URL to connect')

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    cmd = RestCmd(**vars(args))
    cmd.cmdloop()
