# Import dependencies
import http.cookiejar
import os
import uuid
from tls_client import Session


# Define the function to get a token
def get_token():

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

    # Set headers for the token request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',  # Setting to Firefox
        'Authorization': 'Basic bm9haWhkZXZtXzZpeWcwYThsMHE6',  # Seems to be the same across all browsers on PC
        'ETP-Anonymous-ID': f'{uuid.uuid4()}',  # Device ID, can be a randomized UUID
        'Origin': 'https://www.crunchyroll.com',  # Crunchyroll origin
        'Referer': 'https://www.crunchyroll.com/',  # Crunchyroll referer
    }

    # Set data for the token request
    data = {
        'device_id': f'{uuid.uuid4()}',  # Device ID, can be randomized UUID
        'device_type': 'Firefox on Windows',  # Setting to FireFox
        'grant_type': 'etp_rt_cookie',  # Not sure what that is
    }

    # Send a post request to the auth login
    response = session.post('https://www.crunchyroll.com/auth/v1/token', headers=headers, data=data)

    # Retrieve the token from the response
    token = f"Bearer {response.json()['access_token']}"

    # Return the token
    return token
