from rest_cmd import RestCmd
import argparse
from cmd2 import with_argparser, with_category


class BindableRestCmd(RestCmd):

    def __init__(self, url_root='http://localhost'):
        self.bound_command = None
        self.bound_command_func = None
        RestCmd.__init__(self, url_root)

    def _set_prompt(self):
        pt_cmd = '{} '.format(self.bound_command) if self.bound_command else ''
        pt_resrc = '/{}'.format(self.resource) if self.resource else ''
        self.prompt = '[{}{}{}] '.format(
            self.colorize(pt_cmd, 'green'),
            self.colorize(self.url_root, 'blue'),
            self.colorize(pt_resrc, 'green'))

    bind_parser = argparse.ArgumentParser(prog='bind')
    bind_subparser = bind_parser.add_subparsers(title='subcommands',
                                                help='subommand help')
    bind_subcommands = {
        'get': {
            'help': 'GET',
            'func': lambda cmd, args: cmd._bind('get', cmd.do_get)
        },
        'post': {
            'help': 'POST',
            'func': lambda cmd, args: cmd._bind('post', cmd.do_post)
        },
        'put': {
            'help': 'PUT',
            'func': lambda cmd, args: cmd._bind('put', cmd.do_put)
        },
        'patch': {
            'help': 'PATCH',
            'func': lambda cmd, args: cmd._bind('patch', cmd.do_patch)
        },
        'delete': {
            'help': 'DELETE',
            'func': lambda cmd, args: cmd._bind('delete', cmd.do_delete)
        },
        'head': {
            'help': 'HEAD',
            'func': lambda cmd, args: cmd._bind('head', cmd.do_head)
        },
        'options': {
            'help': 'OPTIONS',
            'func': lambda cmd, args: cmd._bind('options', cmd.do_options)
        }
    }

    for subcmd, params in bind_subcommands.items():
        subcmd_parser = bind_subparser.add_parser(subcmd, help=params['help'])
        subcmd_parser.set_defaults(func=params['func'])
    bind_parser.set_defaults(func=lambda cmd, args: cmd.do_help('bind'))

    @with_argparser(bind_parser)
    @with_category(RestCmd.CMD_REST_SUPPORT)
    def do_bind(self, args):
        """Bind a command to skip typing"""
        args.func(self, args)

    def _bind(self, cmd_name, cmd_func):
        if cmd_name and cmd_func:
            self.bound_command = cmd_name
            self.bound_command_func = cmd_func
            self._set_prompt()
        else:
            self.perror('command not specified')

    @with_category(RestCmd.CMD_REST_SUPPORT)
    def do_unbind(self, args):
        """Unbind a command"""
        if self.bound_command:
            self._unbind_command()
        else:
            self.perror('command not bound')

    def _unbind_command(self):
        self.bound_command = None
        self.bound_command_func = None
        self._set_prompt()

    def default(self, statement):
        if self.bound_command_func:
            self.bound_command_func(statement.raw)
        else:
            super().default(statement)
