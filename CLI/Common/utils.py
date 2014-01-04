import argparse
import os
import sys
import textwrap
import uuid
import json

import prettytable
import six

from CLI.Common import importutils

def prettyPrint(retVal):
    print json.dumps(retVal,sort_keys=False,indent=4, separators=(',', ': '))

class HelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def define_command(subparsers, command, callback, cmd_mapper):
    '''Define a command in the subparsers collection.

    :param subparsers: subparsers collection where the command will go
    :param command: command name
    :param callback: function that will be used to process the command
    '''
    desc = callback.__doc__ or ''
    help = desc.strip().split('\n')[0]
    arguments = getattr(callback, 'arguments', [])

    subparser = subparsers.add_parser(command, help=help,
                                      description=desc,
                                      add_help=False,
                                      formatter_class=HelpFormatter)
    subparser.add_argument('-h', '--help', action='help',
                           help=argparse.SUPPRESS)
    cmd_mapper[command] = subparser
    for (args, kwargs) in arguments:
        subparser.add_argument(*args, **kwargs)
    subparser.set_defaults(func=callback)


def define_commands_from_module(subparsers, command_module, cmd_mapper):
    '''Find all methods beginning with 'do_' in a module, and add them
    as commands into a subparsers collection.
    '''
    for method_name in (a for a in dir(command_module) if a.startswith('do_')):
        # Commands should be hypen-separated instead of underscores.
        command = method_name[3:].replace('_', '-')
        callback = getattr(command_module, method_name)
        define_command(subparsers, command, callback, cmd_mapper)


# Decorator for cli-args
def arg(*args, **kwargs):
    def _decorator(func):
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.__dict__.setdefault('arguments', []).insert(0, (args, kwargs))
        return func
    return _decorator


def pretty_choice_list(l):
    return ', '.join("'%s'" % i for i in l)


def print_list(objs, fields, field_labels, formatters={},
               sortby=0):
    pt = prettytable.PrettyTable([f for f in field_labels],
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                #data = getattr(o, field, '')
                data = o.get(field)
                row.append(data)
        pt.add_row(row)
    print(pt.get_string(sortby=field_labels[sortby]))
    
def print_dict_as_list(objs, fields, field_labels, formatters={},
               sortby=0):
    pt = prettytable.PrettyTable([f for f in field_labels],
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for o in objs.values():
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                data = o.get(field)
                row.append(data)
        pt.add_row(row)
    print(pt.get_string(sortby=field_labels[sortby]))


def print_dict(d, dict_property="Property", wrap=0):
    pt = prettytable.PrettyTable([dict_property, 'Value'],
                                 caching=False, print_empty=False)
    pt.align = 'l'
    for k, v in six.iteritems(d):
        # convert dict to str to check length
        if isinstance(v, dict):
            v = six.text_type(v)
        if wrap > 0:
            v = textwrap.fill(six.text_type(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, six.string_types) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            pt.add_row([k, v])
    print(pt.get_string())


def find_resource(manager, name_or_id):
    """Helper for the _find_* methods."""
    # first try to get entity as integer id
    try:
        if isinstance(name_or_id, int) or name_or_id.isdigit():
            return manager.get(int(name_or_id))
    except:
        pass

    # now try to get entity as uuid
    try:
        uuid.UUID(str(name_or_id))
        return manager.get(name_or_id)
    except:
        pass

    # finally try to find entity by name
    try:
        return manager.find(name=name_or_id)
    except:
        msg = (_("No %(class)s with a name or ID of '%(nameid)s' exists") %
                {'class': manager.resource_class.__name__.lower(),
                 'nameid': name_or_id})
        raise CommandError(msg)


def string_to_bool(arg):
    return arg.strip().lower() in ('t', 'true', 'yes', '1')


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def import_versioned_module(version, submodule=None):
    module = 'CLI.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)



def exit(msg=''):
    if msg:
        print(msg)
    sys.exit(1)
    
def bool_or_string(string):
    if string in ['True', 'true', 'TRUE']:
        return True
    if string in ['False', 'false', 'FALSE']:
        return False
    else:
        return str(string)