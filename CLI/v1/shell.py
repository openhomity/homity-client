from CLI.Common import utils
from CLI.v1 import pin_shell
from CLI.v1 import spoke_shell


COMMAND_MODULES = [
    pin_shell,
    spoke_shell
]


def enhance_parser(parser, subparsers, cmd_mapper):
    '''Take a basic (nonversioned) parser and enhance it with
    commands and options specific for this version of API.

    :param parser: top level parser :param subparsers: top level
        parser's subparsers collection where subcommands will go
    '''
    for command_module in COMMAND_MODULES:
        utils.define_commands_from_module(subparsers, command_module,
                                          cmd_mapper)