# Import dependencies
import glob
import subprocess
import PySimpleGUI as sg
import config.assets.icons
import os
from . import thumbnail_helper
from . import metadata_helper
from . import keys_helper
from . import pssh_helper
from . import manifest_helper
from . import segment_helper
from . import video_token_helper
from . import command_helper
from . import subtitle_helper


# Define the function to start the GUI
def start_gui():

    # Set the theme
    sg.theme('Dark Grey11')

    # Set the top layout
    top_layout = [sg.Text('URL: '), sg.Input(key='-CRUNCHYROLL_URL-', expand_x=True, expand_y=True),
                  sg.Button(button_text='Load', key='-LOAD_BUTTON-'), sg.Button(button_text='Reset', key='-RESET_BUTTON-', disabled=True)]

    # Set items to be in the left frame
    left_frame_items = [
        [sg.Text(text="MPD:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-MPD-', expand_x=True, expand_y=True)],
        [sg.Text(text="PSSH:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-PSSH-', expand_x=True, expand_y=True)],
        [sg.Text(text="Content ID:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-CONTENT_ID-', expand_x=True, expand_y=True)],
        [sg.Text(text="Video Token:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-VIDEO_TOKEN-', expand_x=True, expand_y=True)],
        [sg.Text(text='Keys:', expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-DECRYPTION_KEYS-', expand_x=True, expand_y=True)],
    ]

    # Set the left frame
    left_frame = sg.Frame(title="Widevine Information", layout=left_frame_items, expand_x=True, expand_y=True)

    # Set items to be in the right frame
    right_frame_items = [
        [sg.Text(text="Preview", expand_x=True, expand_y=True, justification='center')],
        [sg.Image(source="", key='-THUMBNAIL-', expand_x=True, expand_y=True)],
        [sg.Text(text="Series:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-SERIES-', expand_x=True, expand_y=True)],
        [sg.Text(text="Season:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-SEASON-', expand_x=True, expand_y=True)],
        [sg.Text(text="Episode:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-EPISODE-', expand_x=True, expand_y=True)],
        [sg.Text(text="Title:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-TITLE-', expand_x=True, expand_y=True)],
        [sg.Text(text="Language:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", disabled=True, no_scrollbar=True, key='-LANGUAGE-', expand_x=True, expand_y=True)],
        [sg.Text(text="Description:", expand_x=True, expand_y=True)],
        [sg.Multiline(default_text="", size=(1, 8), disabled=True, no_scrollbar=True, key='-DESCRIPTION-', expand_x=True, expand_y=True)],
    ]

    # Set the right frame
    right_frame = sg.Frame(title="Metadata", layout=right_frame_items, expand_x=True, expand_y=True)

    # Set the first bottom layout
    first_bottom_layout = [sg.Button(button_text='Download', key='-DOWNLOAD_BUTTON-', disabled=True), sg.Combo(default_value="", readonly=True, key='-AVAILABLE_RESOLUTIONS-', values=[], expand_x=True, expand_y=True, disabled=True), sg.Combo(default_value="", readonly=True, key='-AVAILABLE_SUBTITLES-', values=[], expand_x=True, expand_y=True, disabled=True), sg.Input(default_text=f'{os.getcwd()}/downloads/completed', disabled=True, expand_x=True, expand_y=True, disabled_readonly_text_color='Black', key='-DOWNLOAD_LOCATION-'), sg.FolderBrowse(button_text='Browse', target='-DOWNLOAD_LOCATION-', key='-BROWSE_BUTTON-')]

    # Set the second bottom layout
    second_bottom_layout = [sg.Multiline(default_text="", disabled=True, text_color="Black", key="-CONSOLE-", auto_refresh=True, no_scrollbar=True, expand_x=True, expand_y=True, visible=False, autoscroll=True, do_not_clear=True, size=(5, 5))]

    # define the layout
    layout = [
        [top_layout],
        [left_frame, right_frame],
        [first_bottom_layout],
        [second_bottom_layout]
    ]

    # create the window
    window = sg.Window('TPD Crunchy Downloader', layout, resizable=True, icon=config.assets.icons.taskbar_icon)

    # start the event loop
    while True:

        # Read the event that happened and the values dictionary
        event, values = window.read()

        # Print out event and values for debugging
        # print(event, values)

        # Event handler for load button
        if event == '-LOAD_BUTTON-':

            # Check if the crunchyroll URL is right
            if segment_helper.get_url_segment(url=values['-CRUNCHYROLL_URL-']) is not False:

                # Get the manifest
                manifest_url, manifest_content, manifest_language, manifest_subtitles = manifest_helper.get_manifest(
                    url=values['-CRUNCHYROLL_URL-'])

                # Get the PSSH
                pssh = pssh_helper.parse_pssh(manifest_url=manifest_url)

                # Get content ID
                content_id = segment_helper.get_url_segment(url=values['-CRUNCHYROLL_URL-'])

                # Get the video token
                video_token = video_token_helper.get_video_token(url=values['-CRUNCHYROLL_URL-'])

                # Get the keys
                keys, _ = keys_helper.get_keys(pssh=pssh, content_id=content_id, video_token=video_token)

                # Get the thumbnail
                thumbnail = thumbnail_helper.convert_thumbnail(url=values['-CRUNCHYROLL_URL-'])

                # Get the metadata
                series_name, season_number, episode_number, title, description = metadata_helper.get_metadata(
                    url=values['-CRUNCHYROLL_URL-'])

                # Get available resolutions
                available_resolutions = metadata_helper.get_available_resolutions(manifest=manifest_content)

                # Get available subtitles
                available_subtitles = []
                for subtitle in manifest_subtitles:
                    available_subtitles.append(subtitle)

                # Update the window

                # Update the URL input field
                window['-CRUNCHYROLL_URL-'].update(disabled=True)

                # Update the load button
                window['-LOAD_BUTTON-'].update(disabled=True)

                # Update the reset button
                window['-RESET_BUTTON-'].update(disabled=False)

                # Update the MPD
                window['-MPD-'].update(value=manifest_url)

                # Update the PSSH
                window['-PSSH-'].update(value=pssh)

                # Update the Content ID
                window['-CONTENT_ID-'].update(value=content_id)

                # Update the Video Token
                window['-VIDEO_TOKEN-'].update(value=video_token)

                # Update the keys
                window['-DECRYPTION_KEYS-'].update(value=keys)

                # Update thumbnail
                window['-THUMBNAIL-'].update(source=thumbnail)

                # Update series name
                window['-SERIES-'].update(value=series_name)

                # Update the season number
                window['-SEASON-'].update(value=season_number)

                # Update the episode number
                window['-EPISODE-'].update(value=episode_number)

                # Update the title
                window['-TITLE-'].update(value=title)

                # Update the language
                window['-LANGUAGE-'].update(value=manifest_language)

                # Update the description
                window['-DESCRIPTION-'].update(value=description)

                # Update the download button
                window['-DOWNLOAD_BUTTON-'].update(disabled=False)

                # Update the download button
                window['-AVAILABLE_RESOLUTIONS-'].update(values=available_resolutions, set_to_index=[1], disabled=False)

                # Update the download button
                window['-AVAILABLE_SUBTITLES-'].update(values=available_subtitles, disabled=False, set_to_index=[0])

            else:
                sg.Popup('Invalid URL!', 'Make sure your URL starts with https://www.crunchyroll.com/watch/', custom_text="Okay")



        # Event handler for reset button
        if event == '-RESET_BUTTON-':

            # Update the URL input field
            window['-CRUNCHYROLL_URL-'].update(disabled=False, value='',)

            # Update the load button
            window['-LOAD_BUTTON-'].update(disabled=False)

            # Update the load button
            window['-RESET_BUTTON-'].update(disabled=True)

            # Update the MPD
            window['-MPD-'].update(value='')

            # Update the PSSH
            window['-PSSH-'].update(value='')

            # Update the Content ID
            window['-CONTENT_ID-'].update(value='')

            # Update the Video Token
            window['-VIDEO_TOKEN-'].update(value='')

            # Update the keys
            window['-DECRYPTION_KEYS-'].update(value='')

            # Update thumbnail
            window['-THUMBNAIL-'].update(source='')

            # Update series name
            window['-SERIES-'].update(value='')

            # Update the season number
            window['-SEASON-'].update(value='')

            # Update the episode number
            window['-EPISODE-'].update(value='')

            # Update the title
            window['-TITLE-'].update(value='')

            # Update the language
            window['-LANGUAGE-'].update(value='')

            # Update the description
            window['-DESCRIPTION-'].update(value='')

            # Update the download button
            window['-DOWNLOAD_BUTTON-'].update(disabled=True)

            # Update the download button
            window['-BROWSE_BUTTON-'].update(disabled=False)

            # Update the download button
            window['-AVAILABLE_RESOLUTIONS-'].update(values=[], disabled=False)

            # Update available subtitles
            window['-AVAILABLE_SUBTITLES-'].update(values=[], disabled=False)

            # Update the console visibility
            window['-CONSOLE-'].update(visible=False)

        # Event handler for download button
        if event == '-DOWNLOAD_BUTTON-':

            # Update the console visibility
            window['-CONSOLE-'].update(visible=True)

            # Get the PSSH
            pssh = values['-PSSH-']

            # Get the MPD
            mpd = values['-MPD-']

            # Get the download location
            download_location = values['-DOWNLOAD_LOCATION-']

            # Get the content ID
            content_id = values['-CONTENT_ID-']

            # Get the video token
            video_token = values['-VIDEO_TOKEN-']

            # Get the mp4decrypt keys
            _, mp4decryptkeys = keys_helper.get_keys(pssh=pssh, content_id=content_id, video_token=video_token)

            # Get the series name
            series_name = values['-SERIES-']

            # Get the season number
            season_number = values['-SEASON-']

            # Get the episode
            episode_number = values['-EPISODE-']

            # Get the episode title
            episode_title = values['-TITLE-']

            # Get the language
            language = values['-LANGUAGE-']

            # Get the episode description
            episode_description = values['-DESCRIPTION-']

            # Get the resolution
            available_resolutions = values['-AVAILABLE_RESOLUTIONS-']

            # Get the subtitle choice
            subtitle_choice = values['-AVAILABLE_SUBTITLES-']

            # Disable the download button
            window['-DOWNLOAD_BUTTON-'].update(disabled=True)

            # Disable the browse button
            window['-BROWSE_BUTTON-'].update(disabled=True)

            # Disable available resolutions
            window['-AVAILABLE_RESOLUTIONS-'].update(disabled=True)

            # Disable available subtitles
            window['-AVAILABLE_SUBTITLES-'].update(disabled=True)

            # Generate the download command
            download_command = command_helper.generate_nm3u8dlre_command(mpd=mpd, download_location=download_location, series_name=series_name,
                                                            season_number=season_number, episode_number=episode_number, episode_title=episode_title,
                                                            resolution=available_resolutions, language=language, mp4decryptkeys=mp4decryptkeys)

            # Iterate over the download command generator and parse to the console window
            for window_update in command_helper.run_nm3u8dlre_subprocess_with_output(nm3u8dlre_command=download_command):
                window['-CONSOLE-'].update(value=window_update, append=True)

            # Grab the subtitles
            _, _, _, manifest_subtitles = manifest_helper.get_manifest(url=values['-CRUNCHYROLL_URL-'])

            # Download the subtitles
            subtitles = subtitle_helper.download_subs(manifest_subtitles=manifest_subtitles, episode_title=episode_title, sub_lang=subtitle_choice)

            # Generate the subtitle mux command
            ffmpeg_command = command_helper.generate_ffmpeg_command(mkv_location=download_location, mkv_name=f'{series_name} - Season {season_number} Episode {episode_number} - {episode_title}', mkv_subtitles=subtitles)

            # Run the subtitle mux command
            subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            # Grab all files in the subtitle folder
            subtitle_files = glob.glob(os.path.join(f'{os.getcwd()}/downloads/subtitles', '*'))

            # Iterate through the files and delete them
            for files in subtitle_files:
                os.remove(files)

            # Delete the old video
            os.remove(f'{download_location}/{series_name} - Season {season_number} Episode {episode_number} - {episode_title} - No Subs.mkv')

            # Rename the file
            os.rename(f'{download_location}/{series_name} - Season {season_number} Episode {episode_number} - {episode_title} - With Subs.mkv', f'{download_location}/{series_name} - Season {season_number} Episode {episode_number} - {episode_title}.mkv')

            # Print finished on the console
            window['-CONSOLE-'].update(value=f"Finished\n\n", append=True)

        # Event handler for native close button
        if event == sg.WIN_CLOSED:
            break

    window.close()
