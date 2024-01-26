# Import dependencies
import os


# Define the function to check and create all required folders
def check_and_create_folders():

    # Check for binaries folder
    if 'binaries' not in os.listdir(fr'{os.getcwd()}'):
        os.makedirs(f'{os.getcwd()}/binaries')

    # Check for config folder
    if 'config' not in os.listdir(fr'{os.getcwd()}'):
        os.makedirs(f'{os.getcwd()}/config')
        os.makedirs(f'{os.getcwd()}/config/assets')
        os.makedirs(f'{os.getcwd()}/config/cookies')
        os.makedirs(f'{os.getcwd()}/config/database')

    # Check for config sub folders if config folder is found
    if 'config' in os.listdir(fr'{os.getcwd()}'):
        if 'assets' not in os.listdir(fr'{os.getcwd()}/config'):
            os.makedirs(f'{os.getcwd()}/config/assets')
        if 'cookies' not in os.listdir(fr'{os.getcwd()}/config'):
            os.makedirs(f'{os.getcwd()}/config/cookies')
        if 'database' not in os.listdir(fr'{os.getcwd()}/config'):
            os.makedirs(f'{os.getcwd()}/config/database')

    # Check for downloads folder
    if 'downloads' not in os.listdir(fr'{os.getcwd()}'):
        os.makedirs(f'{os.getcwd()}/downloads')
        os.makedirs(f'{os.getcwd()}/downloads/completed')
        os.makedirs(f'{os.getcwd()}/downloads/temp')
        os.makedirs(f'{os.getcwd()}/downloads/subtitles')

    # Check for config sub folders if downloads folder is found
    if 'downloads' in os.listdir(fr'{os.getcwd()}'):
        if 'completed' not in os.listdir(fr'{os.getcwd()}/downloads'):
            os.makedirs(f'{os.getcwd()}/downloads/completed')
        if 'temp' not in os.listdir(fr'{os.getcwd()}/downloads'):
            os.makedirs(f'{os.getcwd()}/downloads/temp')
        if 'subtitles' not in os.listdir(fr'{os.getcwd()}/downloads'):
            os.makedirs(f'{os.getcwd()}/downloads/subtitles')