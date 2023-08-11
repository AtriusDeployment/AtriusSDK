from requests import exceptions
from requests_toolbelt.multipart.encoder import MultipartEncoder


# API Resource Paths
V1_PATH = 'api/rest/v1'
V2_PATH = 'api/rest/v2'


# Base URL for the Eclypse APIs
def api_base_url(hostname, version=1):
    if version == 1:
        return f'https://{hostname}/{V1_PATH}'
    if version == 2:
        return f'https://{hostname}/{V2_PATH}'


# REST methods
def api_post(session, host, path, body, version=1):
    """POST to API"""
    url = f'{api_base_url(host, version)}{path}'
    headers = {'Content-type': 'application/json'}
    result = session.post(url, json=body, headers=headers)
    result.raise_for_status()
    return result


def api_get(session, host, path, version=1): # Throws requests error
    """GET from API"""
    url = f'{api_base_url(host, version)}{path}'
    headers = {'accept': 'application/json'}

    result = session.get(url, headers=headers, timeout=30)
    result.raise_for_status()
    return result

# Downloading files from a store requires a different header
def api_get_store(session, host, path, version=1): # Throws requests error
    """GET from API"""
    url = f'{api_base_url(host, version)}{path}'
    headers = { 'Accept': '*/*' }

    result = session.get(url, headers=headers)
    result.raise_for_status()
    return result

def api_put(session, host, path, body, version=1):
    """PUT to API"""
    url = f'{api_base_url(host, version)}{path}'
    headers = {'Content-type': 'application/json'}
    result = session.put(url, json=body, headers=headers)
    result.raise_for_status()
    return result


def api_delete(session, host, path, version=1):
    """Delete via API"""
    url = f'{api_base_url(host, version)}{path}'
    headers = {'Content-type': 'application/json'}
    result = session.delete(url, headers=headers)
    result.raise_for_status()
    return result


def get_info_device(session, host):
    """Get ECLYPSE device information"""
    return api_get(session, host, '/info/device')


def api_version(session, host):
    """Returns the ECY API Version based on a successful call"""
    headers = {'accept': 'application/json'}

    try:
        v1_url = f'{api_base_url(host, 1)}'
        v1_result = session.get(v1_url, headers=headers, timeout=30)
        if v1_result.ok:
            return 1

        v2_url = f'{api_base_url(host, 2)}/services'
        v2_result = session.get(v2_url, headers=headers, timeout=30)
        if v2_result.ok:
            return 2
    except exceptions.ConnectTimeout as e:
        # Raise an exception if the specified host did not respond
        raise e
        


def get_services_v1(session, host):
    """Returns list of ECY 1 services"""
    return api_get(session, host, '', version=1)


def get_services_v2(session, host):
    """Returns list of ECY 2 services"""
    # Note: this list can change as packages extend the API
    return api_get(session, host, '/services', version=2)


# Hostname

def get_hostname(session, host):
    method = "/system/web-server"
    return api_get(session, host, method)


def set_hostname(session, host, hostname):
    method = "/system/web-server"
    data = {'hostname': hostname}
    return api_post(session, host, method, data)


# MSTP

def get_mstp(session, host, port=1):
    method = f'/protocols/bacnet/communication/network/mstp-ports/{int(port)}'
    return api_get(session, host, method)


def set_mstp(session, host, data, port=1):
    method = f'/protocols/bacnet/communication/network/mstp-ports/{int(port)}'
    return api_post(session, host, method, data)


def enable_mstp(session, host):
    data = {'enabled': True}
    return set_mstp(session, host, data, port=1)


def disable_mstp(session, host):
    data = {'enabled': False}
    return set_mstp(session, host, data, port=1)


def set_mstp_priority(session, host):
    data = {'id': 1, 'priority': 50}
    return set_mstp(session, host, data, port=1)


# BACnet IP
def get_bacnet_ip(session, host, port=1):
    method = f'/protocols/bacnet/communication/network/ip-ports/{int(port)}'
    return api_get(session, host, method)


def set_bacnet_ip(session, host, data, port=1):
    method = f'/protocols/bacnet/communication/network/ip-ports/{int(port)}'
    return api_post(session, host, method, data)


def enable_bacnet_ip(session, host):
    data = {'enabled': True}
    return set_bacnet_ip(session, host, data, port=1)


def disable_bacnet_ip(session, host):
    data = {'enabled': False}
    return set_bacnet_ip(session, host, data, port=1)


# Wifi
def get_wifi(session, host, port='primary'):
    method = f'/system/network/adapters/wireless/{port}'
    return api_get(session, host, method)


def set_wifi(session, host, data, port='primary'):
    method = f'/system/network/adapters/wireless/{port}'
    return api_post(session, host, method, data)


def enable_wifi(session, host):
    data = {'enabled': True, 'mode': 'hotspot'}
    return set_wifi(session, host, data, port='primary')


def disable_wifi(session, host):
    data = {'enabled': False}
    return set_wifi(session, host, data, port='primary')


# Firmware

def get_eclypse_firmware_version(session, host):
    return get_info_device(session, host)['softwareVersion']


def update_eclypse_firmware(session, host, update_file):
    path = "/system/update/firmware"
    url = f'{api_base_url(host)}{path}'

    m = MultipartEncoder(fields={'file': (update_file, open(update_file, 'rb'), 'application/octet-stream')})

    return session.post(url, data=m, headers={'Content-Type': m.content_type})


def reboot_controller(session, host):
    path = "/protocols/bacnet/local/management/coldStart"
    data = {}

    return api_post(session, host, path, data)


# Time

def get_time(session, host):
    path = "/system/date-time"
    return api_get(session, host, path)


def set_time(session, host, data):
    method = "/system/date-time"

    return api_post(session, host, method, data)


def change_time_zone(session, host, timezone):
    data = {'timeZone': timezone, 'autoTime': True}

    return set_time(session, host, data)

