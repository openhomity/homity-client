from CLI.Common import utils
from collections import OrderedDict
from Client.HomityHubClient import HomityHubClientError


def _print_spoke_show(spoke):
    fields = ['id', 'name', 'active', 'driver', 'driver_info']
    data = OrderedDict([(f, spoke.get(f)) for f in fields])
    utils.print_dict(data, wrap=72)
    
@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
def do_spoke_show(cc, args):
    """Show an spoke's pin."""
    spoke = cc.spoke(spoke_id=args.spoke)
    _print_spoke_show(spoke)

@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
def do_spoke_pin_list(cc, args):
    """List pins for an spoke."""
    pins = cc.spoke(spoke_id=args.spoke, path=["pins"])
    field_labels = ['UUID', 'Name', 'Num', 'Allocated', 'Digital', 'Output', 'Status']
    fields = ['id', 'name', 'num', 'allocated', 'digital', 'output', 'status']
    utils.print_dict_as_list(pins, fields, field_labels, sortby=1)
    
def do_spoke_list(cc, args):
    """List spokes."""
    spokes = cc.spoke()
    field_labels = ['UUID', 'Name', 'Active', 'Driver']
    fields = ['id', 'name', 'active', 'driver']
    utils.print_list(spokes, fields, field_labels, sortby=1)
    
def do_spoke_driver_list(cc, args):
    """List available spoke drivers."""
    spoke_drivers = cc.spoke_drivers()
    print spoke_drivers
    
@utils.arg('name', metavar='<spoke name>', help="Name of spoke")
@utils.arg('driver', metavar='<driver name>', help="Name of driver")
@utils.arg('driver_info', metavar='<driver_arg=value>', nargs='+', action='append', default=[], help="Driver_Info Attributes")
def do_spoke_create(cc, args):
    """Create a new spoke."""
    driver_info = {}
    for attribute in args.driver_info[0]:
        path, value = attribute.split("=", 1)
        driver_info[path] = value
    
    try:
        spoke = cc.spoke_create(args.name, args.driver, driver_info)
    except HomityHubClientError as e:
        print e
    _print_spoke_show(spoke)
    
@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
def do_spoke_delete(cc, args):
    """Delete a spoke."""
    cc.spoke_delete(args.spoke)
    
    """List spokes."""
    spokes = cc.spoke()
    field_labels = ['UUID', 'Name', 'Active', 'Driver']
    fields = ['id', 'name', 'active', 'driver']
    utils.print_list(spokes, fields, field_labels, sortby=1)
    
@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+', action='append', default=[], help="Attributes to change")
def do_spoke_update(cc, args):
    """Update a spoke's settings."""
    for attribute in args.attributes[0]:
        pathkey, value = attribute.split("=", 1)
        path = pathkey.split("/")
        cc.spoke(spoke_id=args.spoke, path=path, value=utils.bool_or_string(value))
    try:
        spoke = cc.spoke(spoke_id=args.spoke)
    except HomityHubClientError as e:
        print e
    _print_spoke_show(spoke)
