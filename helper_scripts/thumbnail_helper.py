# Import dependencies
import http.cookiejar
import os
import requests
from tls_client import Session
from PIL import Image
from io import BytesIO
from . import token_helper
from . import segment_helper


# Define the function to get thumbnail
def get_thumbnail(url: str = None):

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

    # Get the thumbnail
    thumbnail = requests.get(url=response.json()['data'][0]['images']['thumbnail'][0][0]['source']).content

    # Return the thumbnail
    return thumbnail


# Define the function to convert thumbnail to PNG
def convert_thumbnail(url: str = None):

    # Get the thumbnail data
    thumbnail = get_thumbnail(url=url)

    # Open the JPEG image from the in-memory content
    with Image.open(BytesIO(thumbnail)) as image:

        # Create an in-memory buffer for the PNG image
        png_buffer = BytesIO()

        # Convert and save as PNG to the in-memory buffer
        image.save(png_buffer, 'PNG')

        # Get the PNG content from the buffer
        png_content = png_buffer.getvalue()

    # return the PNG
    return png_content
