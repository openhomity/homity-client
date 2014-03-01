"""Helpers for shell tests."""
from commands import getoutput

def do_list_shell(cmd):
    """Execute cmd at the shell.  Return cleaned output."""
    output = getoutput(cmd)
    return parse_list(output)

def do_item_shell(cmd):
    """Execute cmd at the shell.  Return cleaned output."""
    output = getoutput(cmd)
    return parse_dict(output)

def parse_list(output):
    """Parse PrettyTable list output into list of dict."""
    
def parse_dict(output):
    """Parse PrettyTable dict output into dict."""
    
    