
    
@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
def test_spoke_show():

@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
def test_spoke_pin_list():

@utils.arg('-f', '--filters', metavar='<key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def test_spoke_list():
    
def test_spoke_driver_list():
    
@utils.arg('name', metavar='<spoke name>', help="Name of spoke")
@utils.arg('driver', metavar='<driver name>', help="Name of driver")
@utils.arg('driver_info', metavar='<driver_arg=value>', nargs='+', action='append', default=[], help="Driver_Info Attributes")
def test_spoke_create():
    
@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
def test_spoke_delete():
    
@utils.arg('spoke', metavar='<spoke id>', help="UUID of spoke")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+', action='append', default=[], help="Attributes to change")
def test_spoke_update():


@utils.arg('pin', metavar='<pin id>', help="UUID of pin")
def test_pin_show():


@utils.arg('-f', '--filters', metavar='<key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def test_pin_list():


@utils.arg('pin', metavar='<pin id>', help="UUID of pin")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+', action='append', default=[], help="Attributes to change")
def test_pin_update():

    
@utils.arg('pin', metavar='<pin id>', help="UUID of pin")
@utils.arg('minute', metavar='<minute>', help="Minute of hour - e.g. 30")
@utils.arg('hour', metavar='<hour>', help="Hour of day in 24hr - e.g. 15")
@utils.arg('days', metavar='<days>', help="Days of week - e.g. 0-6, 0 = Sunday")
@utils.arg('action', metavar='<action>', help="Action to perform - True or False")
def test_pin_schedule_add():


@utils.arg('pin', metavar='<pin id>', help="UUID of pin") 
@utils.arg('index', metavar='<schedule index>', help="List index of schedule entry")
def test_pin_schedule_delete():

