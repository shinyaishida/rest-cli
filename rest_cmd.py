from cmd2 import Cmd
from cmd2 import with_argument_list, with_category, with_argparser
import argparse
import requests
from time import sleep


class RestCmd(Cmd):
    CMD_REST_ACTION = 'REST Action Commands'
    CMD_REST_SUPPORT = 'REST Support Commands'

    def __init__(self, url_root='http://localhost'):
        Cmd.__init__(self)
        self.allow_cli_args = False
        self._format_url_root(url_root)
        self.resource = ''
        self._set_prompt()
        self.response = None

    def _format_url_root(self, url_root):
        self.url_root = url_root[:-1] if url_root.endswith('/') else url_root

    def _set_prompt(self):
        self.prompt = '[{}/{}] '.format(
            self.colorize(self.url_root, 'green'),
            self.colorize(self.resource, 'blue'))

    OPTIONS = {
        '-r': {'metavar': 'N', 'dest': 'count', 'type': int, 'default': 1,
               'help': 'iteration count (1 by default)'},
        '-i': {'dest': 'interval', 'type': float, 'default': 0.5,
               'help': 'iteration interval in seconds (0.5 by default)'},
        'resource': {'metavar': 'RESOURCE', 'nargs': '?',
                     'help': 'resource to send request(s)'}
    }

    repeatable_parser = argparse.ArgumentParser()
    for option, option_params in OPTIONS.items():
        repeatable_parser.add_argument(option, **option_params)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_get(self, args):
        """Send GET request"""
        self._iterate(lambda x: requests.get(x), args)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_post(self, args):
        """Send POST request"""
        self._iterate(lambda x: requests.post(x), args)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_put(self, args):
        """Send PUT request"""
        self._iterate(lambda x: requests.put(x), args)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_patch(self, args):
        """Send PATCH request"""
        self._iterate(lambda x: requests.patch(x), args)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_delete(self, args):
        """Send DELETE request"""
        self._iterate(lambda x: requests.delete(x), args)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_head(self, args):
        """Send HEAD request"""
        self._iterate(lambda x: requests.head(x), args)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_ACTION)
    def do_options(self, args):
        """Send OPTION request"""
        self._iterate(lambda x: requests.options(x), args)

    def _iterate(self, request, args):
        org_resource = self.resource
        if args.resource:
            self.resource = self._switch_resource(args.resource)
        for i in range(args.count):
            self._record_response(request)
            sleep(args.interval)
        self.resource = org_resource

    def _record_response(self, request):
        self.response = request(self._get_url())
        self.poutput(self.response)

    def _get_url(self):
        return self.url_root + ('/{}'.format(self.resource) if self.resource else '')

    response_parser = argparse.ArgumentParser(prog='response')
    response_subparser = response_parser.add_subparsers(title='subcommands',
                                                        help='subcommand help')
    response_subcommands = {
        'content': {'help': 'print body as bytes',
                    'func': lambda cmd, args: cmd.poutput(cmd.response.content)},
        'encoding': {'help': 'print encoding',
                     'func': lambda cmd, args: cmd.poutput(cmd.response.encoding)},
        'headers': {'help': 'print headers',
                    'func': lambda cmd, args: cmd.poutput(cmd.response.headers)},
        'json': {'help': 'decode to JSON format',
                 'func': lambda cmd, args: cmd.poutput(cmd.response.json())},
        'status': {'help': 'print status code',
                   'func': lambda cmd, args: cmd.poutput(cmd.response.status_code)},
        'text': {'help': 'print text',
                 'func': lambda cmd, args: cmd.poutput(cmd.response.text)},
        'url': {'help': 'print URL',
                'func': lambda cmd, args: cmd.poutput(cmd.response.url)}
    }

    for subcmd, params in response_subcommands.items():
        subcmd_parser = response_subparser.add_parser(subcmd,
                                                      help=params['help'])
        subcmd_parser.set_defaults(func=params['func'])
    response_parser.set_defaults(func=lambda cmd, args: cmd.do_help('response'))

    @with_argparser(response_parser)
    @with_category(CMD_REST_ACTION)
    def do_response(self, args):
        """Review last response"""
        if self.response:
            args.func(self, args)
        else:
            self.perror('send a requst before running respond command')

    @with_argument_list
    @with_category(CMD_REST_SUPPORT)
    def do_switch(self, args):
        """Change URL root"""
        if args:
            self._format_url_root(args[0])
            self._set_prompt()

    @with_argument_list
    @with_category(CMD_REST_SUPPORT)
    def do_cd(self, args):
        """Change target resource"""
        self.resource = self._switch_resource(args[0]) if args else ''
        self._set_prompt()

    def _switch_resource(self, resource):
        if not resource:
            return ''
        path = self.resource
        levels = list(filter(lambda x: x, resource.split('/')))
        for level in levels:
            if level == '..':
                if path:
                    tokens = path.split('/')
                    path = '/'.join(tokens[:-1])
                else:
                    self.perror('invalid resource {0}'.format(resource))
                    path = self.resource
                    break
            elif level != '.':
                path = (path + '/' if path else path) + level
        return path
