import eclypse
from requests import exceptions
from requests_toolbelt.multipart.encoder import MultipartEncoder


# Packages (aka. DCARS)
# Packages are found in BI under settings -> packages
# Packages extend the functionallity of the BI platform
# Packages are independantly versioned, installed, and upgraded
# Packages may depend on a specific version of other packages
# The file containing a package typically has the .dcar extension
# May be referred to as DCAR (Distech Controls ARchive)

def list_packages(session, host):
    """List all installed packages"""
    path = '/services/packages'
    return eclypse.api_get(session, host, path, version=2)


def upload_package(session, host, package):
    """Upload a file containing a package"""
    method = "/services/packages/store"

    with open(package, 'rb') as open_file:
        data = open_file.read()

    return eclypse.api_post_store(session, host, method, data, version=2)


def commit_all(session, host):
    """Commit changes to the installed packages - install, uninstall, upgrade"""
    path = '/services/packages/commit'
    data = {
            'operations': [
                {
                'type': 'Install',
                'item': '*'
                }
            ]
            }
    
    return eclypse.api_post(session, host, path, data, version=2)


def commit_package(session, host, package):
    """Commit a specific package by name"""
    path = '/services/packages/commit'
    data = {
            'operations': [
                {
                'type': 'Install',
                'item': package
                }
            ]
            }
    
    return eclypse.api_post(host, path, data, version=2)

