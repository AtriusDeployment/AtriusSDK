import concurrent.futures
import requests
import util
import argparse
import gfx


# If True, do not display SSL certificate verification warnings
SUPPRESS_SSL_WARNING = False


def gfx_version(site):
    """Retrieve GFX Project Name"""
    # Split input values
    hostname, username, password = site.values()

    # Create a session to make multiple requests
    with requests.session() as session:
        # ECLYPSE local API requires HTTP basic authentiation
        session.auth = (username,password)
        # Disable SSL certificate verification when using default self-signed certificate
        session.verify = False

        try:
            # Get current firmware version
            result = gfx.get_project_name(session, hostname)
            return {'host': hostname,'version': result}
        
        # Allow the run to continue when a single ECLYPSE returns an error
        except requests.exceptions.HTTPError:
            return {'host': hostname, 'status': 'Login Failed'}
        except requests.exceptions.ConnectionError:
            return {'host': hostname, 'status': 'Not Responding'}


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Report GFX Version")
    parser.add_argument('host_file', default='./host_file', help='List of ECLYPSE controllers')

    args = parser.parse_args()

    # Disable warning for self-signed certificate
    if SUPPRESS_SSL_WARNING:
        requests.packages.urllib3.disable_warnings()

    # Script requires a list of ECLYPSE in a csv file
    # The csv file should contain information for 1 ECLYPSE per line
    # Required format is:
    # hostname,username,password
    host_list = util.read_host_list(args.host_file)

    # List to hold results for report
    report = []

    # Concurrent futures manages the query of multiple ECLYPSE at the same time
    # max_workers determines the number of workers 
    # increase max_workers to decrease runtime
    # decrease max_workers to reduce CPU and bandwidth consumption
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs = [executor.submit(gfx_version, site) for site in host_list]

        # Record result as each worker completes an upgrade job
        for job in concurrent.futures.as_completed(jobs):
            # Output result to screen
            if job.result() is not None:
                print(job.result())

            # Add results with data to the report
            if not 'status' in job.result().keys():
                report.append(job.result())

    # Write CSV report
    util.to_csv(report)

if __name__ == "__main__":
    main()
