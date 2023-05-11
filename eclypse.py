from requests_toolbelt.multipart.encoder import MultipartEncoder


# V1 Resource Path
V1_PATH = 'api/rest/v1'

# Base URL for the Eclypse API
def api_base_url(hostname):
    return f'https://{hostname}/{V1_PATH}'


# REST methods
def api_post(session, host, path, body):
    """POST to API"""
    url = f'{api_base_url(host)}{path}'
    headers = {'Content-type': 'application/json'}
    result = session.post(url, json=body, headers=headers)
    result.raise_for_status()
    return result

def api_get(session, host, path): # Throws requests error
    """GET from API"""
    url = f'{api_base_url(host)}{path}'
    headers = {'accept': 'application/json'}

    result = session.get(url, headers=headers, timeout=30)
    result.raise_for_status()
    return result


def get_info_device(session, host):
    """Get ECLYPSE device information"""
    return api_get(session, host, '/info/device')


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

