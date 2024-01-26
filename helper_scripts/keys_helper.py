# Import dependencies
import requests
import base64
from . import token_helper
from . import database_helper


# Define the function to get keys
def get_keys(pssh: str = None, content_id: str = None, video_token: str = None):

    # Set the headers to send to CDM Project CDM API
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Referer': 'https://static.crunchyroll.com/',
        'authorization': f'{token_helper.get_token()}',
        'content-type': 'application/octet-stream',
        'x-cr-content-id': f'{content_id}',
        'x-cr-video-token': f'{video_token}',
        'Origin': 'https://static.crunchyroll.com',
    }

    # Set CDM Project API URL
    api_url = "https://api.cdm-project.com"

    # Set API device
    api_device = "CDM"

    # Set headers for API key
    api_key_headers = {
        "X-Secret-Key": "Crunchyroll"
    }

    # Open CDM session
    open_session = requests.get(url=f'{api_url}/{api_device}/open', headers=api_key_headers)

    # Get the session ID from the open CDM session
    session_id = open_session.json()["data"]["session_id"]

    # Set JSON required to generate a license challenge
    generate_challenge_json = {
        "session_id": session_id,
        "init_data": pssh
    }

    # Generate the license challenge
    generate_challenge = requests.post(url=f'{api_url}/{api_device}/get_license_challenge/AUTOMATIC', headers=api_key_headers, json=generate_challenge_json)

    # Retrieve the challenge and base64 decode it
    challenge = base64.b64decode(generate_challenge.json()["data"]["challenge_b64"])

    # Send the challenge to the widevine license server
    license = requests.post(
        url="https://cr-license-proxy.prd.crunchyrollsvc.com/v1/license/widevine",
        headers=headers,
        data=challenge
    )

    # Retrieve the license message
    license = license.json()["license"]

    # Set JSON required to parse license message
    license_message_json = {
        "session_id": session_id,
        "license_message": license
    }

    # Parse the license
    requests.post(url=f'{api_url}/{api_device}/parse_license', headers=api_key_headers, json=license_message_json)

    # Retrieve the keys
    get_keys = requests.post(url=f'{api_url}/{api_device}/get_keys/ALL',
                             json={"session_id": session_id},
                             headers=api_key_headers)

    # Assign variable for returned keys
    returned_keys = ''

    # Iterate through the keys, ignoring signing key
    for key in get_keys.json()["data"]["keys"]:
        if not key["type"] == "SIGNING":
            returned_keys += f"{key['key_id']}:{key['key']}\n"

    database_helper.cache_keys(pssh=pssh, keys=returned_keys)

    # Assign variable for mp4decrypt keys
    mp4decrypt_keys = []

    # Iterate through the keys and append them to mp4decrypt_keys dictionary
    for key in get_keys.json()["data"]["keys"]:
        if not key["type"] == "SIGNING":
            mp4decrypt_keys.append('--key')
            mp4decrypt_keys.append(f"{key['key_id']}:{key['key']}")

    # Close session
    requests.get(url=f'{api_url}/{api_device}/close/{session_id}', headers=api_key_headers)

    # return returned keys and mp4decrypt keys
    return returned_keys, mp4decrypt_keys
