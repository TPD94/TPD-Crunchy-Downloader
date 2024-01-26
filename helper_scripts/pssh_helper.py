# Import dependencies
import requests
import re
from . import token_helper


# Define MPD / m3u8 PSSH parser
def parse_pssh(manifest_url):

    # Set the headers for the request
    headers = {
        'Authorization': f'{token_helper.get_token()}',
    }

    # Grab the manifest
    response = requests.get(manifest_url, headers=headers)

    # Search for matches based on regular expression search
    matches = re.finditer(r'<cenc:pssh(?P<any>(.*))>(?P<pssh>(.*))</cenc:pssh>', response.text)

    # Initialize PSSH list
    pssh_list = []

    # Iterate through the matches
    for match in matches:
        if match.group and not match.group("pssh") in pssh_list and len(match.group("pssh")) < 300:
            pssh_list.append(match.group("pssh"))

    # If no PSSH added to list, iterate through the matches with a different regular expression search
    if len(pssh_list) < 1:
        matches = re.finditer(r'URI="data:text/plain;base64,(?P<pssh>(.*))"', response.text)
        for match in matches:
            if match.group("pssh") and match.group("pssh").upper().startswith("A") and len(match.group("pssh")) < 300:
                pssh_list.append(match.group("pssh"))

    # Return the PSSH from PSSH list
    return f'{pssh_list[0]}'