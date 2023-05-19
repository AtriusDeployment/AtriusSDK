import json
import io
import xml.etree.ElementTree as ET
import requests
import eclypse
from zipfile import ZipFile, BadZipFile


def get_project(session, host):
    """Retrieve GFX file from ECLYPSE"""
    try:
        api_url = '/files/common/localDevice/project/Project.gfx?encode=bin'
        return eclypse.api_get(session, host, api_url).content
    except:
        return({'exception': 'Unknown Error'})


def get_project_metadata(project):
    """Extract Main.xml project metadata from compressed project"""
    try: 
        zip_file = ZipFile(io.BytesIO(project))
    except BadZipFile:
        return({'exception': 'bad zip file'})

    return zip_file.open("Main.xml")


def get_project_name(session, host):
    """Retrieve project name from project metadata"""
    project = get_project(session, host)

    project_file = get_project_metadata(project)

    tree = ET.parse(io.BytesIO(project_file.read()))

    root = tree.getroot()

    for project in root:
        if project.tag == 'Project':
            for props in project:
                if props.tag == 'Props':
                    for name in props:
                        if name.tag == 'Name':
                            return name.text


def get_version_atrius(session, host):
    """Retrieve version number exposed as points in the Atrius specific GFX"""
    major_url = "https://" + host + "/api/rest/v1/protocols/bacnet/local/objects/analog-value/5000/properties/present-value"
    major = session.get(major_url)

    minor_url = "https://" + host + "/api/rest/v1/protocols/bacnet/local/objects/analog-value/5001/properties/present-value"
    minor = session.get(minor_url)

    revision_url = "https://" + host + "/api/rest/v1/protocols/bacnet/local/objects/analog-value/5002/properties/present-value"
    revision = session.get(revision_url)

    return major.json()['value'], minor.json()['value'], revision.json()['value']


def upload_gfx(session, host, gfx_file):
    """Upload GFX, note: requires a pre-compiled GFX in zip format"""
    update_url = "https://" + host + "/api/rest/v1/files/bacnet/inputConfiguration"
    gfx_file_handle= {'file': open(gfx_file, 'rb')}

    result = session.post(update_url, files=gfx_file_handle).json()
    return result


def halt_gfx_engine(session, host):
    """Halt GFX engine"""
    method = "/protocols/bacnet/local/objects/Program/1/properties/programChange"
    payload = {'value': 'Halt'}
    
    result = eclypse.api_post(session, host, method, payload).json()
    return result


def unload_gfx_engine(session, host):
    """"Unload GFX"""
    method = "/protocols/bacnet/local/objects/Program/1/properties/programChange"
    payload = {'value': 'Unload'}

    result = eclypse.api_post(host, method, payload).json()
    return result


def load_gfx_engine(session, host):
    """Load GFX"""
    method = "/protocols/bacnet/local/objects/Program/1/properties/programChange"
    payload = {'value': 'Load'}
    
    result = eclypse.api_post(session, host, method, payload).json()
    return result


def check_gfx_engine_busy(session, host):
    """Check the config manager status, Bool"""
    # Busy while loading new logic
    method = "/engine/config-manager"

    result = eclypse.api_get(session, host, method).json()
    return result['Busy']


def check_program_state(session, host):
    """Check GFX engine status, Running/Stopped"""
    # Result of halt
    method = "/protocols/bacnet/local/objects/program/1/properties/program-state"

    result = eclypse.api_get(session, host, method).json()
    return result['value']


if __name__ == '__main__':
    pass