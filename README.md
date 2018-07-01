rest-cli
====

`rest-cli` is a CLI to send HTTP requests (GET, POST, PUT, PATCH, DELETE, HEAD,
OPTIONS) easier than `curl`. Since `rest-cli` is stateful, you can

- omit inputting a (part of) URL to request,
- omit inputting a request command by binding it,
- inspect the content of a response after receiving it,
- repeat a same request by referring command history or by the repeat option,
- and more.

## Installation

`rest-cli` is written in Python 3. It is recommended to use
[pyenv](https://github.com/pyenv/pyenv) so as not to affect your other local
Python projects.

``` bash
$ pyenv install 3.6.4
$ git clone https://github.com/shinyaishida/rest-cli.git
$ cd rest-cli
$ pip install cmd2 requests
```

## Basic usage

This section briefly introduces a way to send an HTTP request and get its
response. `rest-cli` is based on
[`cmd2`](http://cmd2.readthedocs.io/en/latest/). So, it inherits the useful
features of `cmd2`, such as tab-completion, history, backward history search,
and so on.

### Start CLI

The following command starts the CLI with the default URL, `http://localhost`.
The current target URL is shown in the command prompt.

``` bash
$ python rest_cli.py
[http://localhost/]
```

If you want to access another URL than the default one, specify it as an
argument. The URL you specified appears in the command prompt.

``` bash
$ python rest_cli.py http://server.you.want.to.access:port
[http://server.you.want.to.access:port/]
```

You can see the usage by `python rest_cli.py -h`.

### Learn available commands

`help` command gives you a list of available commands. REST Action Commands is a
group of commands to send HTTP requests and to inspect their responses. REST
Support Commands is a group of commands to reduce the overhead to input REST
action commands on the terminal. The Other group contains the `cmd2` built-in
commands.

``` bash
[http://localhost/] help

Documented commands (type help <topic>):

REST Action Commands
====================
delete  get  head  options  patch  post  put  response

REST Support Commands
=====================
bind  cd  switch  unbind

Other
=====
alias  help     load  pyscript  set    shortcuts
edit   history  py    quit      shell  unalias
```

### Send a request and inspect its response

Requests are send by REST action commands; `get`, `post`, `put`, `patch`,
`delete`, `head`, and `options`. If you execute `get` command as shown below,
the CLI sends a GET request to the URL indicated in the prompt. You will see
the status code on the terminal if you receive a response from the web server.

``` bash
[http://localhost/] get
<Response [xxx]>
```

You can inspect the content of the response using `response` command. It has
subcommands to indicate a part of the response message to print on the
terminal.

``` bash
[http://localhost] response -h
usage: response [-h] {content,encoding,headers,json,status,text,url} ...

Review last response

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {content,encoding,headers,json,status,text,url}
                        subcommand help
    content             print body as bytes
    encoding            print encoding
    headers             print headers
    json                decode to JSON format
    status              print status code
    text                print text
    url                 print URL
```

If you want to get a resource under the URL printed in the prompt, say
`http://localhost/foo`, specify the relative path to the resource from the root
as an argument.

``` bash
[http://localhost/] get foo
```

### Terminate CLI

``` bash
[http://localhost/] quit
```

## Advanced usage

`rest-cli` provides support commands to help you reduce the overhead to input
request commands. It also provides useful options of request commands to
simplify your operations.

### Fixing target resource and request command

You can change the target URL by `cd` command, which behaves
like the `cd` command of shells for POSIX systems. You do not need to specify
`foo` to get (or do something else with) the resource.

``` bash
[http://localhost/] cd foo
[http://localhost/foo] get
```

As you would guess, you can change the target URL back to the original one as
follows.

``` bash
[http://localhost/foo] cd ..
[http://localhost/]
```

`cd` command cannot go above the URL that you specified on starting the CLI. To
change the original URL, use `switch` command instead.

``` bash
$ python rest_cli.py http://localhost/foo/bar
[http://localhost/foo/bar/] cd ..
ERROR: invalid resource ..
[http://localhost/foo/bar/] switch http://localhost/foo
[http://localhost/foo/]
```

The two support commands introduced above let you shorten or omit the input of
target resources on sending requests. Similarly, there is a support command,
`bind`, to fix a request command (`get`, `post`, `put`, `patch`, `delete`,
`head`, or `options`). When you execute `bind` command, the prompt shows the
request command you bound.

``` bash
[http://localhost/foo/] bind get
[get http://localhost/foo/]
```

If you want to get the resource `http://localhost/foo/bar`, what you need to do
is just hit `bar` and the enter key.

``` bash
[get http://localhost/foo/] bar
<Response [xxx]>
```

You can change the bound command by `bind` command. Use `unbind` command to
unbind the bound command.

``` bash
[get http://localhost/] bind post
[post http://localhost/] unbind
[http://localhost/]
```

### Repeating a same request

You may sometimes want to send a same request multiple times, automatically.
The request commands have `-r` option to specify how many times to send the
request. The following example sends a GET request twice.

``` bash
[http://localhost/] get -r2
<Response [xxx]>
<Response [xxx]>
```

Note that frequent requests may make the web server get overloaded. The CLI
uses a modest interval by default (0.5 seconds) to avoid it but you can change
the interval by `-i` option.

``` bash
[http://localhost/] get -r2 -i0.01
```

If you bound `get` command, the input command becomes shorter.

``` bash
[get http://localhost/] -r2 -i0.01
```

## Todos

- script file execution
- save history as a script
- request/response logger
- key4remote

## Author

[shinyaishida](https://github.com/shinyaishida)

## License

[GPLv3](LICENSE)
