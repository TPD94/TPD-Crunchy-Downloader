# Import dependencies
import PySimpleGUI as sg
import os
import config.assets.icons


# Define the function to check and create binaries
def check_if_cookies():

    # Set the window theme
    sg.theme('Dark Grey11')

    # Create a layout for progress bar window
    error_layout = [
        [sg.Text('Downloading N_m3u8DL-RE')],
    ]

    # Check for cookies.txt
    if not os.path.isfile(path=f'{os.getcwd()}/config/cookies/cookies.txt'):
        sg.Popup('No cookies found!', f'Please place your cookies in {os.getcwd()}/config/cookies.txt', custom_text="Okay")
        return False
    else:
        return True

