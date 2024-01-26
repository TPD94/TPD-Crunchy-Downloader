# Import dependencies
import http.cookiejar
import os
import xml.etree.ElementTree as ET
from tls_client import Session
from . import token_helper
from . import segment_helper


# Define the function to get metadata
def get_metadata(url: str = None):

    # Set the configuration options for the session
    session = Session(
        client_identifier="firefox_120",
        random_tls_extension_order=True
    )

    # Load Mozilla Cookie jar function as cookie_jar
    cookie_jar = http.cookiejar.MozillaCookieJar()

    # Load cookies.txt from /config/cookies/cookies.txt
    cookie_jar.load(f"{os.getcwd()}/config/cookies/cookies.txt")

    # Set cookies to the session
    session.cookies = cookie_jar

    # Set headers for the CMS (Content Management System) request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'{token_helper.get_token()}',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': f'{url}'
    }

    # Send a get request to the CMS (Content Management System) API
    response = session.get(
        f'https://www.crunchyroll.com/content/v2/cms/objects/{segment_helper.get_url_segment(url=url)}',
        headers=headers)

    # Retrieve the series name
    series_name = response.json()['data'][0]['episode_metadata']['series_title']

    # Retrieve the season number
    season_number = response.json()['data'][0]['episode_metadata']['season_number']

    # Retrieve the episode number
    episode_number = response.json()['data'][0]['episode_metadata']['episode']

    # Retrieve the title
    title = response.json()['data'][0]['title']

    # Retrieve the description
    description = response.json()['data'][0]['description']

    # Return the token
    return series_name, season_number, episode_number, title, description


# Define the function to get available resolutions
def get_available_resolutions(manifest: bytes = None):

    # Parse the XML string
    root = ET.fromstring(manifest)

    available_heights = []

    # Iterate through Representations
    for representation in root.findall('.//ns:Representation', {'ns': 'urn:mpeg:dash:schema:mpd:2011'}):
        height = representation.get('height')
        codecs = representation.get('codecs')
        if codecs.startswith("avc1."):
            available_heights.append(f'{height}p')

    return available_heights
