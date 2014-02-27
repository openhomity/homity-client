"""Homity Hub CLI."""
import argparse
import logging

from Client.HomityHubClient import HomityHubClient, HomityHubClientError
from CLI.Common import utils
from CLI.Common import exc

class HomityHubCLI(object):
    """Class for Homity CLIs."""
    def get_base_parser(self):
        """Top level parser."""
        parser = argparse.ArgumentParser(
            prog='homity',
            description="Homity CLI",
            epilog='See "homity help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=HelpFormatter,
        )

        # Global arguments
        parser.add_argument('-h', '--help',
                            action='store_true',
                            help=argparse.SUPPRESS,
                            )

        parser.add_argument('-d', '--debug',
                            default=False,
                            action='store_true',
                            help='Defaults to False')

        parser.add_argument('-v', '--verbose',
                            default=False, action="store_true",
                            help="Print more verbose output")

        parser.add_argument('--timeout',
                            default=600,
                            help='Number of seconds to wait for a response')

        return parser

    def get_subcommand_parser(self, version=""):
        """Grab child parsers."""
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        submodule = utils.import_versioned_module(version, 'shell')
        submodule.enhance_parser(parser, subparsers, self.subcommands)
        utils.define_commands_from_module(subparsers, self, self.subcommands)
        return parser

    def _setup_debugging(self, debug):
        """Turn on debugging."""
        if debug:
            logging.basicConfig(
                format="%(levelname)s (%(module)s:%(lineno)d) %(message)s",
                level=logging.DEBUG)

        else:
            logging.basicConfig(
                    format="%(levelname)s %(message)s",
                    level=logging.CRITICAL)

    def main(self, argv, client_config):
        """Do stuff."""
        # Parse args once to find version
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self._setup_debugging(options.debug)

        # build available subcommands based on version
        subcommand_parser = self.get_subcommand_parser("1")
        self.parser = subcommand_parser

        # Handle top-level --help/-h before attempting to parse
        # a command off the command line
        if options.help or not argv:
            self.do_help(options)
            return 0

        # Parse args again and call whatever callback was selected
        args = subcommand_parser.parse_args(argv)

        # Short-circuit and deal with help command right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0

        client = HomityHubClient(hostname=client_config.get('hostname'),
                                 username=client_config.get('username'),
                                 password=client_config.get('password'),
                                 use_ssl=client_config.get('use_ssl'),
                                 verify_ssl=client_config.get('verify_ssl'),
                                 stateless=True,
                                 version=1)

        args.func(client, args)

    @utils.arg('command', metavar='<subcommand>', nargs='?',
               help='Display help for <subcommand>')
    def do_help(self, args):
        """Display help about this program or one of its subcommands."""
        if getattr(args, 'command', None):
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()


class HelpFormatter(argparse.HelpFormatter):
    """Format help prints."""
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)
        