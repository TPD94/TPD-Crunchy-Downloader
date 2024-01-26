# Import dependencies
from urllib.parse import urlparse


# Define function to return asset ID from URL
def get_url_segment(url: str = None):

    # Parse the URL
    parsed_url = urlparse(url)

    # Set the path segments
    path_segments = parsed_url.path.split('/')

    # Find the index of 'watch' in the path
    try:
        watch_index = path_segments.index('watch')
    except:
        return False

    # Extract the string between 'watch' and the next path segment
    url_segment = path_segments[watch_index + 1]

    # Return the URL segment
    return url_segment
