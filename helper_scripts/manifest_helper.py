# Import dependencies
import requests
from . import token_helper
from . import segment_helper


# Define the function to get the manifest
def get_manifest(url: str = None):

    # Set bearer token to reduce spam
    auth_beaerer = f'{token_helper.get_token()}'

    # Set the headers for the request
    headers = {
        'Authorization': f'{auth_beaerer}',
    }

    # Send a get request for the manifest
    response = requests.get(f'https://cr-play-service.prd.crunchyrollsvc.com/v1/{segment_helper.get_url_segment(url=url)}/web/firefox/play',
                            headers=headers)

    # Extract manifest from JSON
    manifest_url = response.json()['url']

    # Extract the audio language
    manifest_language = response.json()['audioLocale']

    # Extract the subtitles
    manifest_subtitles = response.json()['subtitles']

    # Extract the content from the manifest
    manifest_content = requests.get(f'{manifest_url}',
                            headers=headers).content

    # Return the URL and content
    return manifest_url, manifest_content, manifest_language, manifest_subtitles
