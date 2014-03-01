"""Client library for Homity Hub."""
import requests
from requests.auth import HTTPBasicAuth
import json

"""
import logging
import httplib
httplib.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
"""
#logging.basicConfig(level=logging.DEBUG)


class HomityHubClientError(Exception):
    """Handle client errors."""
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

class HomityHubClient(object):
    """Client object for Homity Hub."""
    RESPONSE_CODES = {
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error',
        501: 'Internal Server Error (not implemented)'
    }

    def __init__(self, hostname, username, password,
                 use_ssl=True, verify_ssl=True, version=1):
        self.hostname = hostname
        self.protocol = "http"
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.version = "/v%s" % str(version)
        if use_ssl:
            self.protocol = "https"
        self.base_uri = "%s://%s%s" % (self.protocol,
                                       self.hostname,
                                       self.version)

    def send_get(self, location, params):
        """Send a GET."""
        url = "/".join([self.base_uri, location])
        headers = {'content-type': 'x-www-form-urlencoded'}

        req = requests.get(url,
                         verify=self.verify_ssl,
                         params=params,
                         headers=headers,
                         auth=HTTPBasicAuth(self.username, self.password))
        return self.decode_response(req)

    def send_delete(self, location, params):
        """Send a DELETE."""
        url = "/".join([self.base_uri, location])
        headers = {'content-type': 'x-www-form-urlencoded'}

        req = requests.delete(url,
                            verify=self.verify_ssl,
                            params=params,
                            headers=headers,
                            auth=HTTPBasicAuth(self.username, self.password))
        return self.decode_response(req)

    def send_put(self, location, params):
        """Send a PUT."""
        url = "/".join([self.base_uri, location])
        headers = {'content-type': 'x-www-form-urlencoded'}

        req = requests.put(url,
                           verify=self.verify_ssl,
                           params=params,
                           headers=headers,
                           auth=HTTPBasicAuth(self.username, self.password))
        return self.decode_response(req)

    def send_post(self, location, params):
        """Send a POST."""
        url = "/".join([self.base_uri, location])
        headers = {'content-type': 'application/json'}

        req = requests.post(url,
                          verify=self.verify_ssl,
                          data=json.dumps(params),
                          headers=headers,
                          auth=HTTPBasicAuth(self.username, self.password))
        return self.decode_response(req)

    def decode_response(self, response):
        """
        Handle the response object, and raise exceptions if errors are found.
        """
        url = response.url
        if response.status_code not in (200, 201, 202, 304):
            http_status_code = response.status_code
            raise HomityHubClientError('Got HTTP response code %d - %s for %s, %s' %
                                       (http_status_code,
                                        self.RESPONSE_CODES.get(http_status_code,
                                                                'Unknown!'),
                                        url,
                                        response.text))

        try:
            json_data = json.loads(response.text)
            return json_data
        except:
            return ""

    def spoke_drivers(self):
        """Get list of spoke drivers."""
        location = "spokedrivers"
        return self.send_get(location,
                             params={})

    def spoke(self, spoke_id=None, path=None, value=None):
        """GET/PUT for spoke."""
        if path == None:
            path = []
        if spoke_id != None:
            path.insert(0, spoke_id)
        path.insert(0, "spoke")
        location = '/'.join(path)

        if value != None:
            decoded_json_response = self.send_put(location,
                                                  params={"value":value})
        else:
            decoded_json_response = self.send_get(location,
                                                  params={})

        return decoded_json_response

    def spoke_create(self, name=None, driver=None, driver_info=None):
        """Create a spoke."""
        location = "spoke"
        return self.send_post(location,
                              params={"name":name,
                                      "driver":driver,
                                      "driver_info":driver_info})

    def spoke_delete(self, spoke_id=None, path=None):
        """Delete a spoke."""
        if path == None:
            path = []
        if spoke_id != None:
            path.insert(0, spoke_id)
            path.insert(0, "spoke")
            location = '/'.join(path)
            return self.send_delete(location,
                                    params={})

    def pin_delete(self, pin_id=None, path=None):
        """Delete a pin property."""
        if path == None:
            path = []
        if pin_id != None:
            path.insert(0, pin_id)
            path.insert(0, "pin")
            location = '/'.join(path)
            return self.send_delete(location,
                                    params={})

    def pin_schedule(self, pin_id, new_entry=None, entry_index=None):
        """Add or delete schedule entry for pin."""
        if new_entry == None:
            new_entry = {}
        if new_entry != {} and entry_index != None: #can't create & delete
            return False
        elif entry_index != None: #delete the entry
            return self.pin_delete(pin_id=pin_id,
                                   path=["schedule",
                                         entry_index])
        elif new_entry != None:
            if "minute" and "hour" and "days" and "action" in new_entry:
                new_entry_string = ':'.join([new_entry['minute'],
                                             new_entry['hour'],
                                             new_entry['days'],
                                             new_entry['action']])
                return self.pin(pin_id=pin_id,
                                path=["schedule"],
                                value=new_entry_string)
        return False

    def pin(self, pin_id=None, path=None, value=None):
        """GET/PUT for pin object."""
        if path == None:
            path = []
        if pin_id != None:
            path.insert(0, pin_id)
        path.insert(0, "pin")
        location = '/'.join(path)

        if value != None:
            decoded_json_response = self.send_put(location,
                                                  params={"value":value})
        else:
            decoded_json_response = self.send_get(location,
                                                  params={})

        return decoded_json_response

    def garage_controller_drivers(self):
        """Grab garage controller driver list."""
        location = "garagecontrollerdrivers"
        return self.send_get(location, params={})

    def garage_controller(self, garage_controller_id=None,
                          path=None, value=None):
        """GET/PUT for garage controller."""
        if path == None:
            path = []
        if garage_controller_id != None:
            path.insert(0, garage_controller_id)
        path.insert(0, "garagecontroller")
        location = '/'.join(path)

        if value != None:
            decoded_json_response = self.send_put(location,
                                                  params={"value":value})
        else:
            decoded_json_response = self.send_get(location,
                                                  params={})

        return decoded_json_response

    def garage_controller_create(self, name=None,
                                 driver=None, driver_info=None):
        """Create a new garage controller."""
        location = "garagecontroller"
        return self.send_post(location, params={"name":name,
                                                "driver":driver,
                                                "driver_info":driver_info})

    def garage_controller_delete(self, garage_controller_id=None, path=None):
        """Delete a garage controller."""
        if path == None:
            path = []
        if garage_controller_id:
            path.insert(0, garage_controller_id)
            path.insert(0, "garagecontroller")
            location = '/'.join(path)
            return self.send_delete(location, params={})

    def garage(self, garage_id=None, path=None, value=None):
        """GET/PUT for garage."""
        if path == None:
            path = []
        if garage_id != None:
            path.insert(0, garage_id)
        path.insert(0, "garage")
        location = '/'.join(path)

        if value != None:
            decoded_json_response = self.send_put(location,
                                                  params={"value":value})
        else:
            decoded_json_response = self.send_get(location,
                                                  params={})

        return decoded_json_response

    def camera_controller_drivers(self):
        """Grab camera controller driver list."""
        location = "cameracontrollerdrivers"
        return self.send_get(location, params={})

    def camera_controller(self, camera_controller_id=None,
                          path=None, value=None, **kwargs):
        """GET/PUT for camera controller."""
        if path == None:
            path = []
        if camera_controller_id != None:
            path.insert(0, camera_controller_id)
        path.insert(0, "cameracontroller")
        location = '/'.join(path)

        if value != None:
            decoded_json_response = self.send_put(location,
                                                  params={"value":value})
        else:
            decoded_json_response = self.send_get(location,
                                                  params=kwargs)

        return decoded_json_response

    def camera_controller_create(self, name=None,
                                 driver=None, driver_info=None):
        """Create a new camera controller."""
        location = "cameracontroller"
        return self.send_post(location, params={"name":name,
                                                "driver":driver,
                                                "driver_info":driver_info})

    def camera_controller_delete(self, camera_controller_id=None, path=None):
        """Delete a camera controller."""
        if path == None:
            path = []
        if camera_controller_id:
            path.insert(0, camera_controller_id)
            path.insert(0, "cameracontroller")
            location = '/'.join(path)
            return self.send_delete(location, params={})

    def camera(self, camera_id=None, path=None, value=None, **kwargs):
        """GET/PUT for camera."""
        if path == None:
            path = []
        if camera_id != None:
            path.insert(0, camera_id)
        path.insert(0, "camera")
        location = '/'.join(path)

        if value != None:
            decoded_json_response = self.send_put(location,
                                                  params={"value":value})
        else:
            decoded_json_response = self.send_get(location,
                                                  params=kwargs)

        return decoded_json_response

