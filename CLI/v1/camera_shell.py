"""."""
from CLI.Common import utils
from collections import OrderedDict

def _print_camera_controller_show(camera_controller):
    fields = ['id', 'name', 'active', 'driver', 'driver_info']
    data = OrderedDict([(f, camera_controller.get(f)) for f in fields])
    utils.print_dict(data, wrap=72)

def _print_camera_show(camera):
    fields = ['id', 'location', 'name', 'description', 'allocated',
              'on', 'recording', 'alerts', 'controller']
    data = OrderedDict([(f, camera.get(f)) for f in fields])
    utils.print_dict(data, wrap=72)

@utils.arg('camera', metavar='<camera id>', help="UUID of camera")
def do_camera_show(cc, args):
    """Show a camera."""
    camera = cc.camera(camera_id=args.camera)
    _print_camera_show(camera)

@utils.arg('-f', '--filters', metavar='<key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def do_camera_list(cc, args):
    """List cameras."""
    if len(args.filters) > 0:
        filters = {}
        for entry in args.filters[0]:
            key, value = entry.split("=", 1)
            filters[key] = value
            cameras = cc.camera(**filters)
    else:
        cameras = cc.camera()
    field_labels = ['UUID', 'Controller UUID', 'Location', 'Name',
                    'Description', 'Allocated', 'On', 'Recording', 'Alerts']
    fields = ['id', 'controller', 'location', 'name',
              'description', 'allocated', 'on', 'recording', 'alerts']
    utils.print_list(cameras, fields, field_labels, sortby=1)

@utils.arg('camera', metavar='<camera id>', help="UUID of camera")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def do_camera_update(cc, args):
    """Update a camera."""
    for attribute in args.attributes[0]:
        pathkey, value = attribute.split("=", 1)
        path = pathkey.split("/")
        cc.camera(camera_id=args.camera, path=path, value=value)

    camera = cc.camera(camera_id=args.camera)
    _print_camera_show(camera)

@utils.arg('camera_controller', metavar='<camera_controller id>',
           help="UUID of camera_controller")
def do_camera_controller_show(cc, args):
    """Show a camera_controller."""
    camera_controller = cc.camera_controller(
        camera_controller_id=args.camera_controller)
    _print_camera_controller_show(camera_controller)

@utils.arg('camera_controller', metavar='<camera_controller id>',
           help="UUID of camera_controller")
def do_camera_controller_camera_list(cc, args):
    """List cameras for an camera_controller."""
    cameras = cc.camera_controller(camera_controller_id=args.camera_controller,
                                   path=["cameras"])
    field_labels = ['UUID', 'Controller UUID', 'Location', 'Name',
                    'Description', 'Allocated', 'On', 'Recording', 'Alerts']
    fields = ['id', 'controller', 'location', 'name',
              'description', 'allocated', 'on', 'recording', 'alerts']
    utils.print_dict_as_list(cameras, fields, field_labels, sortby=1)

@utils.arg('-f', '--filters', metavar='<key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def do_camera_controller_list(cc, args):
    """List camera_controller."""
    if len(args.filters) > 0:
        filters = {}
        for entry in args.filters[0]:
            key, value = entry.split("=", 1)
            filters[key] = value
            camera_controllers = cc.camera_controller(**filters)
    else:
        camera_controllers = cc.camera_controller()
    field_labels = ['UUID', 'Name', 'Active', 'Driver']
    fields = ['id', 'name', 'active', 'driver']
    utils.print_list(camera_controllers, fields, field_labels, sortby=1)

def do_camera_controller_driver_list(cc, args):
    """List available camera_controller drivers."""
    camera_controller_drivers = cc.camera_controller_drivers()
    print camera_controller_drivers

@utils.arg('name', metavar='<camera_controller name>',
           help="Name of camera_controller")
@utils.arg('driver', metavar='<driver name>', help="Name of driver")
@utils.arg('driver_info', metavar='<driver_arg=value>', nargs='+',
           action='append', default=[], help="Driver_Info Attributes")
def do_camera_controller_create(cc, args):
    """Create a new camera_controller."""
    driver_info = {}
    for attribute in args.driver_info[0]:
        path, value = attribute.split("=", 1)
        driver_info[path] = value

    camera_controller = cc.camera_controller_create(args.name,
                                                    args.driver,
                                                    driver_info)

    _print_camera_controller_show(camera_controller)

@utils.arg('camera_controller', metavar='<camera_controller id>', help="UUID of camera_controller")
def do_camera_controller_delete(cc, args):
    """Delete a camera_controller."""
    cc.camera_controller_delete(args.camera_controller)

    camera_controllers = cc.camera_controller()
    field_labels = ['UUID', 'Name', 'Active', 'Driver']
    fields = ['id', 'name', 'active', 'driver']
    utils.print_list(camera_controllers, fields, field_labels, sortby=1)

@utils.arg('camera_controller', metavar='<camera_controller id>',
           help="UUID of camera_controller")
@utils.arg('attributes', metavar='<path/key=value>', nargs='+',
           action='append', default=[], help="Attributes to change")
def do_camera_controller_update(cc, args):
    """Update a camera_controller's settings."""
    for attribute in args.attributes[0]:
        pathkey, value = attribute.split("=", 1)
        path = pathkey.split("/")
        cc.camera_controller(camera_controller_id=args.camera_controller,
                             path=path,
                             value=utils.bool_or_string(value))

    camera_controller = cc.camera_controller(camera_controller_id=args.
                                             camera_controller)

    _print_camera_controller_show(camera_controller)

