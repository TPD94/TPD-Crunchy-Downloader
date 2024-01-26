# Import dependencies
import requests
from . import token_helper
from . import segment_helper


# Define the function to get video token
def get_video_token(url: str = None):

    # Set the headers for the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'{token_helper.get_token()}',
        'Origin': 'https://www.crunchyroll.com',
        'Referer': 'https://www.crunchyroll.com/',
    }

    # Send the get request
    response = requests.get(f'https://cr-play-service.prd.crunchyrollsvc.com/v1/{segment_helper.get_url_segment(url=url)}/web/firefox/play',
                            headers=headers)

    # Get video token from JSON response
    video_token = response.json()['token']

    # Return the video token
    return video_token

