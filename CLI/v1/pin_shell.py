from CLI.Common import utils
from collections import OrderedDict

def _print_pin_show(pin):
    fields = ['id','location','name', 'num', 'allocated', 'digital', 'output','schedule', 'allocated', 'status', 'spoke']
    data = OrderedDict([(f, pin.get(f)) for f in fields])
    utils.print_dict(data, wrap=72)

@utils.arg('pin', metavar='<pin id>', help="UUID of pin")
def do_pin_show(cc, args):
    """Show a pin."""
    pin = cc.pin(pin_id=args.pin)
    _print_pin_show(pin)

@utils.arg('-f', '--filters', metavar='<key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def do_pin_list(cc, args):
    """List pins."""
    if len(args.filters) > 0:
        filters = {}
        for entry in args.filters[0]:
            key, value = entry.split("=", 1)
            filters[key] = value
            pins = cc.pin(**filters)
    else:
        pins = cc.pin()
    field_labels = ['UUID', 'Spoke UUID', 'Location', 'Name', 'Num', 'Allocated', 'Digital', 'Output', 'Status']
    fields = ['id', 'spoke', 'location', 'name', 'num', 'allocated', 'digital', 'output', 'status']
    utils.print_list(pins, fields, field_labels, sortby=1)

@utils.arg('pin', metavar='<pin id>', help="UUID of pin")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+', action='append', default=[], help="Attributes to change")
def do_pin_update(cc, args):
    """Update a pin."""
    for attribute in args.attributes[0]:
        pathkey, value = attribute.split("=", 1)
        path = pathkey.split("/")
        cc.pin(pin_id=args.pin, path=path, value=utils.bool_or_string(value))
    
    pin = cc.pin(pin_id=args.pin)
    _print_pin_show(pin)
    
@utils.arg('pin', metavar='<pin id>', help="UUID of pin")
@utils.arg('minute', metavar='<minute>', help="Minute of hour - e.g. 30")
@utils.arg('hour', metavar='<hour>', help="Hour of day in 24hr - e.g. 15")
@utils.arg('days', metavar='<days>', help="Days of week - e.g. 0-6, 0 = Sunday")
@utils.arg('action', metavar='<action>', help="Action to perform - True or False")
def do_pin_schedule_add(cc, args):
    """Insert a new schedule entry."""
    new_entry = {"minute":args.minute, "hour":args.hour, "days":args.days, "action":args.action}
    
    cc.pin_schedule(pin_id=args.pin, new_entry=new_entry)
    
    pin = cc.pin(pin_id=args.pin)
    _print_pin_show(pin)

@utils.arg('pin', metavar='<pin id>', help="UUID of pin") 
@utils.arg('index', metavar='<schedule index>', help="List index of schedule entry")
def do_pin_schedule_delete(cc, args):
    """Delete a schedule entry."""
    cc.pin_schedule(pin_id=args.pin, entry_index=args.index)
    
    pin = cc.pin(pin_id=args.pin)
    _print_pin_show(pin)