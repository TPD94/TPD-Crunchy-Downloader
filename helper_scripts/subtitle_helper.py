# Import dependencies
import os
import requests


# Define function to download subtitles
def download_subs(manifest_subtitles: dict = None, episode_title: str = None, sub_lang: str = None):

    # Create a list to be passed to ffmpeg to merge subtitles later
    subtitle_list = []

    # Iterate through all the subtitles to download and rename
    for language in manifest_subtitles:

        # Check to make sure language is same as chosen
        if language in manifest_subtitles:

            # Create a save name
            save_name = f'{episode_title} {language}.ass'

            # Get the subtitle
            subtitle = requests.get(f'{manifest_subtitles[sub_lang]["url"]}')

            # Save it
            with open(file=f'{os.getcwd()}/downloads/subtitles/{save_name}', mode='w',
                      encoding='utf-8') as subtitle_file:
                subtitle_file.write(subtitle.content.decode())

                # Append the command and location of the subtitles
                subtitle_list.append('-i')
                subtitle_list.append(f'{os.getcwd()}/downloads/subtitles/{save_name}')

    # Return the subtitle list
    return subtitle_list
