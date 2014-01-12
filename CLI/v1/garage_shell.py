from CLI.Common import utils
from collections import OrderedDict

def _print_garage_controller_show(garage_controller):
    fields = ['id', 'name', 'active', 'driver', 'driver_info']
    data = OrderedDict([(f, garage_controller.get(f)) for f in fields])
    utils.print_dict(data, wrap=72)

def _print_garage_show(garage):
    fields = ['id','location','name', 'num', 'allocated', 'open', 'on','controller']
    data = OrderedDict([(f, garage.get(f)) for f in fields])
    utils.print_dict(data, wrap=72)

@utils.arg('garage', metavar='<garage id>', help="UUID of garage")
def do_garage_show(cc, args):
    """Show a garage."""
    garage = cc.garage(garage_id=args.garage)
    _print_garage_show(garage)

def do_garage_list(cc, args):
    """List garages."""
    garages = cc.garage()
    field_labels = ['UUID', 'Controller UUID', 'Location', 'Name', 'Num', 'Allocated', 'On', 'Open']
    fields = ['id', 'controller', 'location', 'name', 'num', 'allocated', 'on', 'open']
    utils.print_list(garages, fields, field_labels, sortby=1)

@utils.arg('garage', metavar='<garage id>', help="UUID of garage")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+', action='append', default=[], help="Attributes to change")
def do_garage_update(cc, args):
    """Update a garage."""
    for attribute in args.attributes[0]:
        pathkey, value = attribute.split("=", 1)
        path = pathkey.split("/")
        cc.garage(garage_id=args.garage, path=path, value=value)
    
    garage = cc.garage(garage_id=args.garage)
    _print_garage_show(garage)

@utils.arg('garage_controller', metavar='<garage_controller id>', help="UUID of garage_controller")
def do_garage_controller_show(cc, args):
    """Show a garage_controller."""
    garage_controller = cc.garage_controller(garage_controller_id=args.garage_controller)
    _print_garage_controller_show(garage_controller)

@utils.arg('garage_controller', metavar='<garage_controller id>', help="UUID of garage_controller")
def do_garage_controller_garage_list(cc, args):
    """List garages for an garage_controller."""
    garages = cc.garage_controller(garage_controller_id=args.garage_controller, path=["garages"])
    field_labels = ['UUID', 'Controller UUID', 'Location', 'Name', 'Num', 'Allocated', 'On', 'Open']
    fields = ['id', 'controller', 'location', 'name', 'num', 'allocated', 'on', 'open']
    utils.print_dict_as_list(garages, fields, field_labels, sortby=1)
    
def do_garage_controller_list(cc, args):
    """List garage_controller."""
    garage_controllers = cc.garage_controller()
    field_labels = ['UUID', 'Name', 'Active', 'Driver']
    fields = ['id', 'name', 'active', 'driver']
    utils.print_list(garage_controllers, fields, field_labels, sortby=1)
    
def do_garage_controller_driver_list(cc, args):
    """List available garage_controller drivers."""
    garage_controller_drivers = cc.garage_controller_drivers()
    print garage_controller_drivers
    
@utils.arg('name', metavar='<garage_controller name>', help="Name of garage_controller")
@utils.arg('driver', metavar='<driver name>', help="Name of driver")
@utils.arg('driver_info', metavar='<driver_arg=value>', nargs='+', action='append', default=[], help="Driver_Info Attributes")
def do_garage_controller_create(cc, args):
    """Create a new garage_controller."""
    driver_info = {}
    for attribute in args.driver_info[0]:
        path, value = attribute.split("=", 1)
        driver_info[path] = value
    
    try:
        garage_controller = cc.garage_controller_create(args.name, args.driver, driver_info)
    except HomityHubClientError as e:
        print e
    _print_garage_controller_show(garage_controller)
    
@utils.arg('garage_controller', metavar='<garage_controller id>', help="UUID of garage_controller")
def do_garage_controller_delete(cc, args):
    """Delete a garage_controller."""
    cc.garage_controller_delete(args.garage_controller)
    
    garage_controllers = cc.garage_controller()
    field_labels = ['UUID', 'Name', 'Active', 'Driver']
    fields = ['id', 'name', 'active', 'driver']
    utils.print_list(garage_controllers, fields, field_labels, sortby=1)
    
@utils.arg('garage_controller', metavar='<garage_controller id>', help="UUID of garage_controller")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+', action='append', default=[], help="Attributes to change")
def do_garage_controller_update(cc, args):
    """Update a garage_controller's settings."""
    for attribute in args.attributes[0]:
        pathkey, value = attribute.split("=", 1)
        path = pathkey.split("/")
        cc.garage_controller(garage_controller_id=args.garage_controller, path=path, value=value)
    try:
        garage_controller = cc.garage_controller(garage_controller_id=args.garage_controller)
    except HomityHubClientError as e:
        print e
    _print_garage_controller_show(garage_controller)
    
