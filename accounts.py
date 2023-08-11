import base64
import eclypse


def get_users_v1(session, host):
    """Return list of existing users"""
    try:
        api_url = '/user-management-v2/users?$expand=*'
        return eclypse.api_get(session, host, api_url).json()
    except Exception as e:
        raise e


def add_user_v1(session, host, username, password):
    """Add a user in Eclypse v1"""
    try:
        api_url = '/user-management-v2/users'
        encoded_password = base64.b64encode(password.encode('utf-8'))

        data = {'username': username,
                'password': encoded_password.decode('utf-8'),
                'passwordReset': False,
                'welcomePage': '',
                'roles': ['admin']}

        return eclypse.api_post(session, host, api_url, data)
        
    except Exception as e:
        raise e


def delete_user_v1(session, host, username):
    """Delete User Eclypse v1"""
    try:
        user_id = get_id_by_name_v1(session, host, username) 
        api_url = f'/user-management-v2/users/{user_id}'

        return eclypse.api_delete(session, host, api_url)
        
    except Exception as e:
        raise e


def get_id_by_name_v1(session, host, username):
    """Get User ID by name"""
    for user in get_users_v1(session, host):
        if username in user.values():
            return str(user['id'])


def set_password_v1(session, host, username, password):
    """Set user password Eclypse v1"""
    try:
        user_id = get_id_by_name_v1(session, host, username) 
        api_url = f'/user-management-v2/users/{user_id}'
        encoded_password = base64.b64encode(password.encode('utf-8'))

        data = {'username': username,
                'password': encoded_password.decode('utf-8'),
                'passwordReset': False}

        # This could also be a PUT
        return eclypse.api_post(session, host, api_url, data)
        
    except Exception as e:
        raise e


def get_users_v2(session, host):
    """Return list of existing users"""
    try:
        api_url = '/services/security/users'
        return eclypse.api_get(session, host, api_url, version=2).json()
    except Exception as e:
        raise e


def add_user_v2(session, host, username, password):
    """Add a user in Ecylypse v2"""
    try:
        api_url = f'/services/security/users/{username}'
            
        data = {'key': username,
                'origin': 'local',
                'roles': [
                    'admin'
                ],
                'language': 'en',
                'units': 'Us',
                'reset-password': False,
                'enabled': True,
                'first-name': '',
                'phone': None,
                'email': '',
                'homepage': None,
                'last-name': '',
                'policy': 'default',
                'password': password}

        return eclypse.api_post(session, host, api_url, data, version=2)
        
    except Exception as e:
        raise e


def delete_user_v2(session, host, username):
    """Delete a user in Ecylypse v2"""
    try:
        api_url = f'/services/security/users/{username}'

        return eclypse.api_delete(session, host, api_url, version=2)
        
    except Exception as e:
        raise e


def set_password_v2(session, host, username, password):
    """Set password Ecylypse v2"""
    try:
        api_url = f'/services/security/users/{username}'
            
        data = {
                'reset-password': False,
                'password': password}

        return eclypse.api_post(session, host, api_url, data, version=2)
        
    except Exception as e:
        raise e


def get_users(session, host, api_version=None):
    """Return list of users from either ECY version"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            users = get_users_v1(session, host)
            return [user['username'] for user in users]
        elif api_version == 2:
            users = get_users_v2(session, host)
            return users.keys()

        raise Exception('Unknown API')

    except Exception as e:
        raise e


def add_user(session, host, username, password, api_version=None):
    """Add user to either API"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            return add_user_v1(session, host, username, password)
        elif api_version == 2:
            return add_user_v2(session, host, username, password)

        raise Exception('Unknown API')

    except Exception as e:
        raise e


def delete_user(session, host, username, api_version=None):
    """Delete user to either API"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            return delete_user_v1(session, host, username)
        elif api_version == 2:
            return delete_user_v2(session, host, username)

        raise Exception('Unknown API')

    except Exception as e:
        raise e


def set_password(session, host, username, password, api_version=None):
    """Add user to either API"""
    try:
        if not api_version:
            api_version = eclypse.api_version(session, host)

        if api_version == 1:
            return set_password_v1(session, host, username, password)
        elif api_version == 2:
            return set_password_v2(session, host, username, password)

        raise Exception('Unknown API')

    except Exception as e:
        raise e


if __name__ == '__main__':

    import requests

    with requests.session() as session:
        session.auth = ('admin','Testpass@1')
        session.verify = False

        username = 'testuser'
        password = 'testpass'
        hostname = '192.168.0.102'

        add_user_v1(session, hostname, username, password)