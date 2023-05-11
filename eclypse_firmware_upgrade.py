import concurrent.futures
import requests
import util
import argparse
import eclypse


# IF True, do not send an older firmware version
# For example, do not downgrade from major version 1.18 to 1.17
PREVENT_DOWNGRADE = True
# If True, do not display SSL certificate verification warnings
SUPPRESS_SSL_WARNING = False


def upgrade(site, update_file, update_version):
    """Upgrade S1000 firmware"""
    # Split input values
    hostname, username, password = site.values()

    # Split the upgrade version for comparrison to current firmware
    uv_major1, uv_major2, uv_minor1, uv_minor2 = update_version.split('.')

    # Create a session to make multiple requests
    with requests.session() as session:
        # ECLYPSE local API requires HTTP basic authentiation
        session.auth = (username,password)
        # Disable SSL certificate verification when using default self-signed certificate
        session.verify = False

        try:
            # Get hardware version
            # This script supports S1000 hardware only
            # To upgrade an APEX hybrid, modify this check and supply APEX specific firmware
            eclypse_info = eclypse.get_info_device(session, hostname).json()
            if 'S1000' not in eclypse_info['modelName'].split(" ")[0]:
                return {'host': hostname,
                        'status': 'Hardware not compatible'}

            # Get current firmware version
            vr_major1, vr_major2, vr_minor1, vr_minor2 = eclypse_info['softwareVersion'].split('.')

            # Skip if already upgraded
            if eclypse_info['softwareVersion'] == update_version:
                return {'host': hostname,
                        'status': f"Skipping - Device is already running {eclypse_info['softwareVersion']}"}

            # Prevent downgrade
            if PREVENT_DOWNGRADE:
                if int(vr_major2) > int(uv_major2):
                    return {'host': hostname,
                            'status': f"Skipping - downgrade from {eclypse_info['softwareVersion']} to {update_version}"}


            # Upgrade
            print({'host': hostname, 'status': f"Uploading - {update_version}"})

            result = eclypse.update_eclypse_firmware(session, hostname, update_file) 

            if result.ok:
                return {'host': hostname, 'status': f"Complete - Uploaded {eclypse_info['softwareVersion']}"}
            
            return {'host': hostname,'status': result.ok}
        
        # Allow the run to continue when a single ECLYPSE upgrade fails.
        except requests.exceptions.HTTPError:
            return {'host': hostname, 'status': 'Login Failed'}
        except requests.exceptions.ConnectionError:
            return {'host': hostname, 'status': 'Not Responding'}


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Upgrade ECLYPSE S1000 Firmware")
    parser.add_argument('host_file', default='./host_file', help='List of ECLYPSE controllers')
    parser.add_argument('update_file', help='Name of the ECLYPSE firmware zip file. ex. ECYSeries_v1.17.22053.807')
    parser.add_argument('update_version', help='Target ECLYPSE firmware version. ex. 1.17.22053.807')

    args = parser.parse_args()

    # Disable warning for self-signed certificate
    if SUPPRESS_SSL_WARNING:
        requests.packages.urllib3.disable_warnings()

    # Script requires a list of ECLYPSE in a csv file
    # The csv file should contain information for 1 ECLYPSE per line
    # Required format is:
    # hostname,username,password
    host_list = util.read_host_list(args.host_file)

    # Concurrent futures manages the upgrade of multiple ECLYPSE at the same time
    # max_workers determines the number of workers executing upgrades
    # increase max_workers to decrease runtime
    # decrease max_workers to reduce CPU and bandwidth consumption
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs = [executor.submit(upgrade, site, args.update_file, args.update_version) for site in host_list]

        # Record result as each worker completes an upgrade job
        for job in concurrent.futures.as_completed(jobs):
            # Output result to screen
            if job.result() is not None:
                print(job.result())


if __name__ == "__main__":
    main()