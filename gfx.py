import io
import xml.etree.ElementTree as ET
from zipfile import ZipFile, BadZipFile
import eclypse


def get_project(session, host):
    """Retrieve GFX file from ECLYPSE"""
    try:
        api_url = '/files/common/localDevice/project/Project.gfx?encode=bin'
        return eclypse.api_get(session, host, api_url).content
    except Exception as e:
        raise e

def get_project_metadata(project):
    """Extract Main.xml project metadata from compressed project"""
    try: 
        zip_file = ZipFile(io.BytesIO(project))
    except BadZipFile as e:
        raise e

    return zip_file.open("Main.xml")


def get_project_name_v1(session, host):
    """Retrieve project name from project metadata"""
    try:
        project = get_project(session, host)

        project_file = get_project_metadata(project)
    except Exception as e:
        raise e

    tree = ET.parse(io.BytesIO(project_file.read()))

    root = tree.getroot()

    for project in root:
        if project.tag == 'Project':
            for props in project:
                if props.tag == 'Props':
                    for name in props:
                        if name.tag == 'Name':
                            return name.text



def get_project_v2(session, host):
    """Get GFX name using V2 API"""
    method = "/services/gfx/programs/1/project"

    result = eclypse.api_get(session, host, method, version=2)
    return result.json()


def get_project_name_v2(session, host):
    """Return the GFX Name"""
    return get_project_v2(session, host)['name']


def get_project_name(session, host, version=None):
    """Return project name"""
    # Attempts v1 and v2 API call for project name

    # If provided, only try the specified API version
    if version == 1:
        return get_project_name_v1(session, host)
    if version == 2:
        return get_project_name_v2(session, host)

    # We will attempt v1 and v2
    # Lack of response is not an exception because we expect 1 call to fail

    # Attempt v1 method
    try:
        return get_project_name_v1(session, host)
    except Exception as e:
        pass

    # Attempt v2 method
    try:
        return get_project_name_v2(session, host)
    except Exception as e:
        pass

    # If we didn't get an answer, raise a exception
    raise Exception("API did not respond")


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