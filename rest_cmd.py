from cmd2 import Cmd
from cmd2 import with_argument_list
from cmd2 import with_category
from cmd2 import argparse, with_argparser
import requests
from time import sleep

CMD_REST_CLI = 'REST CLI Commands'

response_parser = argparse.ArgumentParser(prog='response')
response_subparser = response_parser.add_subparsers(title='subcommands', help='subcommand help')
response_subcommands = {
    'content': {'help': 'print body as bytes'},
    'encoding': {'help': 'print encoding'},
    'headers': {'help': 'print headers'},
    'json': {'help': 'decode to JSON format'},
    'status': {'help': 'print status code'},
    'text': {'help': 'print text'},
    'url': {'help': 'print URL'}
}
for k, v in response_subcommands.items():
    v['func'] = response_subparser.add_parser(k, help=v['help'])

repeatable_parser = argparse.ArgumentParser()
repeatable_parser.add_argument('-r', metavar='N', dest='count', type=int, default=1, help='iteration times')
repeatable_parser.add_argument('-i', dest='interval', type=float, default=0.5, help='iteration interval in sec')

class RestCmd(Cmd):
    def __init__(self, url='http://localhost'):
        Cmd.__init__(self)
        self.url_root = url
        self.resource = ''
        self._set_url()
        self.response = None

    @with_argument_list
    @with_category(CMD_REST_CLI)
    def do_cd(self, args):
        """Change URL hierarchy level"""
        self.resource = self._change_resource(args[0]) if args else ''
        self._set_url()

    def _change_resource(self, resource):
        if not resource:
            return ''
        levels = list(filter(lambda x: x, resource.split('/')))
        path = self.resource
        for level in levels:
            if level == '..':
                if path:
                    tokens = path.split('/')
                    path = '/'.join(tokens[:-1])
                else:
                    print('Error: invalid resource {0}'.format(resource))
                    path = self.resource
                    break
            elif level != '.':
                path = (path + '/' if path else path) + level
        return path

    def _set_url(self):
        self.url = self.url_root + ('/{0}'.format(self.resource) if self.resource else '')
        self.prompt = 'RESTCLI [' + self.url + '] '

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_get(self, args):
        """Send GET request"""
        self._iterate(lambda x: requests.get(x), args.count, args.interval)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_post(self, args):
        """Send POST request"""
        self._iterate(lambda x: requests.post(x), args.count, args.interval)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_put(self, args):
        """Send PUT request"""
        self._iterate(lambda x: requests.put(x), args.count, args.interval)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_patch(self, args):
        """Send PATCH request"""
        self._iterate(lambda x: requests.patch(x), args.count, args.interval)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_delete(self, args):
        """Send DELETE request"""
        self._iterate(lambda x: requests.delete(x), args.count, args.interval)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_head(self, args):
        """Send HEAD request"""
        self._iterate(lambda x: requests.head(x), args.count, args.interval)

    @with_argparser(repeatable_parser)
    @with_category(CMD_REST_CLI)
    def do_options(self, args):
        """Send OPTION request"""
        self._iterate(lambda x: requests.options(x), args.count, args.interval)

    def _iterate(self, request, count, interval):
        for i in range(count):
            self._record_response(request)
            sleep(interval)

    def _record_response(self, request):
        self.response = request(self.url)
        print(self.response)

    @with_argparser(response_parser)
    @with_category(CMD_REST_CLI)
    def do_response(self, args):
        """Review last response"""
        func = getattr(args, 'func', None)
        if func is not None:
            if self.response is not None:
                func(self, args)
            else:
                print('Error: No requests sent')
        else:
            self.do_help('response')

    def _response_content(self, args):
        """Print body of last response as bytes"""
        print(self.response.content)

    def _response_encoding(self, args):
        """Print encoding of last response"""
        print(self.response.encoding)

    def _response_headers(self, args):
        """Print headers of last response"""
        print(self.response.headers)

    def _response_json(self, args):
        """Decode body of last response into the JSON format"""
        print(self.response.json())

    def _response_status(self, args):
        """Print status code of last response"""
        print(self.response.status_code)

    def _response_text(self, args):
        """Print body of last response"""
        print(self.response.text)

    def _response_url(self, args):
        """Print URL of last request"""
        print(self.response.url)

    response_subcommands['content']['func'].set_defaults(func=_response_content)
    response_subcommands['encoding']['func'].set_defaults(func=_response_encoding)
    response_subcommands['headers']['func'].set_defaults(func=_response_headers)
    response_subcommands['json']['func'].set_defaults(func=_response_json)
    response_subcommands['status']['func'].set_defaults(func=_response_status)
    response_subcommands['text']['func'].set_defaults(func=_response_text)
    response_subcommands['url']['func'].set_defaults(func=_response_url)
