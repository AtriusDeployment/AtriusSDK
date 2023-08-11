import eclypse


# API v1
def list_v1(session, hostname):
    """Return list of Eclypse Backups"""
    try:
        api_url = '/system/backup/targets/device/files'
        return eclypse.api_get(session, hostname, api_url).json()

    except Exception as e:
        raise e

        
def create_v1(session, hostname):
    """Schedule a full backup on Eclypse v1"""
    try:
        api_url = '/system/backup/create'
        full_backup = ['TIMEZONE',
                        'WEB_SERVER_CONFIGURATION',
                        'WEATHER',
                        'NETWORK_CONFIGURATION',
                        'USER_MANAGEMENT',
                        'MODULES_FIRMWARES',
                        'CERTIFICATE',
                        'HOSTNAME',
                        'GFX',
                        'BACNET_CONFIGURATION',
                        'PERSISTENCY',
                        'TRENDLOG',
                        'OPENADR']

        data = {'target': 'Device',
                'fileName': hostname.replace('.', '-'),
                'dataTypes': full_backup,
                'envysionProjects': []}

        return eclypse.api_post(session, hostname, api_url, data)
        
    except Exception as e:
        raise e


def latest_v1(session, hostname):
    """Find the latest backup"""
    return sorted([backup['name'] for backup in list_v1(session, hostname)], reverse=True)[0]


def download_v1(session, hostname):
    """Download the latest v1 backup"""
    try:
        latest_backup = latest_v1(session, hostname)
        api_url = f'/files/backup/{latest_backup}.ecybackup?encode=bin'

        return latest_backup, eclypse.api_get_store(session, hostname, api_url, version=1)
        
    except Exception as e:
        raise e


# API v2
def latest_v2(session, hostname):
    """Return the name of the latest backup"""
    backups = [backup for backup in list_v2(session, hostname)]
    latest = sorted(backups, reverse=True)[0]
    return latest


def download_v2(session, hostname):
    """Download the latest v2 backup"""
    try:
        latest_backup = latest_v2(session, hostname)
        api_url = f'/services/backup/store/{latest_backup}'

        return latest_backup, eclypse.api_get_store(session, hostname, api_url, version=2)
        
    except Exception as e:
        raise e


def list_v2(session, hostname):
    """Return list of Eclypse v2 Backups"""
    try:
        api_url = '/services/backup/backups'

        return eclypse.api_get(session, hostname, api_url, version=2).json().keys()

    except Exception as e:
        raise e


def create_v2(session, hostname):
    """Schedule a full backup on Eclypse v2"""
    try:
        api_url = '/services/backup/backups/create'
        data = {
            'option': 'full'
        }

        return eclypse.api_post(session, hostname, api_url, data, version=2)
        
    except Exception as e:
        raise e

# Generic functions call the correct API
def create(session, host, api_version=None):
    """Create a backup"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            return create_v1(session, host)
        elif api_version == 2:
            return create_v2(session, host)

        raise Exception('Unknown API')

    except Exception as e:
        raise e


def list_backups(session, host, api_version=None):
    """List Backups"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            return list_v1(session, host)
        elif api_version == 2:
            return list_v2(session, host)

        raise Exception('Unknown API')

    except Exception as e:
        raise e


def download_backups(session, host, api_version=None):
    """Download Backups"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            return download_v1(session, host)
        elif api_version == 2:
            return download_v2(session, host)

        raise Exception('Unknown API')

    except Exception as e:
        raise e