# Import dependencies
from .import zip_helper
import os
import helper_scripts.download_links
import config.assets.icons
import PySimpleGUI as sg


# Define the function to check and create binaries
def check_and_create_binaries():

    # Set the window theme
    sg.theme('Dark Grey11')

    # Check for nm3u8dlre
    if not os.path.isfile(helper_scripts.download_links.nm3u8dlre['BinaryLocation']):

        # Create a layout for progress bar window
        progress_bar_layout_nm3u8dlre = [
            [sg.Text('Downloading N_m3u8DL-RE')],
            [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS_BAR-')],
        ]

        # Set the progress bar generator for nm3u8dlre
        nm3u8dlre_download_progress = zip_helper.download_binary_zip(url=helper_scripts.download_links.nm3u8dlre['DownloadLink'], zip_name=helper_scripts.download_links.nm3u8dlre['ZipName'])

        # Open up the window and set variable
        window = sg.Window('TPD Crunchy Downloader', progress_bar_layout_nm3u8dlre, resizable=True, icon=config.assets.icons.taskbar_icon, finalize=True)

        # Set variable for the progress bar
        progress_bar = window['-PROGRESS_BAR-']

        # Start the download and update progress bar
        for progress in nm3u8dlre_download_progress:
            progress_bar.update(current_count=(round(progress)))

        # Unzip the binary
        zip_helper.unzip_binary_zip(zip_name=helper_scripts.download_links.nm3u8dlre['ZipName'], unzip_binary_location=helper_scripts.download_links.nm3u8dlre['UnzipBinaryLocation'], unzip_folder_location=helper_scripts.download_links.nm3u8dlre['UnzipFolderLocation'])

        # Close the window once completed
        window.close()

        # return true value for having completed download
        has_nm3u8dlre = True

    # If nm3u8dlre is already present, return true
    if os.path.isfile(helper_scripts.download_links.nm3u8dlre['BinaryLocation']):
        has_nm3u8dlre = True

    # Check for mp4decrypt
    if not os.path.isfile(helper_scripts.download_links.mp4decrypt['BinaryLocation']):

        # Create a layout for progress bar window
        progress_bar_layout_mp4decrypt = [
            [sg.Text('Downloading MP4 Decrypt')],
            [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS_BAR-')],
        ]

        # Set the progress bar generator for mp4decrypt
        mp4decrypt_download_progress = zip_helper.download_binary_zip(url=helper_scripts.download_links.mp4decrypt['DownloadLink'], zip_name=helper_scripts.download_links.mp4decrypt['ZipName'])

        # Open up the window and set variable
        window = sg.Window('TPD Crunchy Downloader', progress_bar_layout_mp4decrypt, resizable=True, icon=config.assets.icons.taskbar_icon, finalize=True)

        # Set variable for the progress bar
        progress_bar = window['-PROGRESS_BAR-']

        # Start the download and update progress bar
        for progress in mp4decrypt_download_progress:
            progress_bar.update(current_count=(round(progress)))

        # Unzip the binary
        zip_helper.unzip_binary_zip(zip_name=helper_scripts.download_links.mp4decrypt['ZipName'], unzip_binary_location=helper_scripts.download_links.mp4decrypt['UnzipBinaryLocation'], unzip_folder_location=helper_scripts.download_links.mp4decrypt['UnzipFolderLocation'])

        # Close the window once completed
        window.close()

        # return true value for having completed download
        has_mp4decrypt = True

    # If mp4decrypt is already present, return true
    if os.path.isfile(helper_scripts.download_links.mp4decrypt['BinaryLocation']):
        has_mp4decrypt = True

    # Check for ffmpeg
    if not os.path.isfile(helper_scripts.download_links.ffmpeg['BinaryLocation']):

        # Create a layout for progress bar window
        progress_bar_layout_ffmpeg = [
            [sg.Text('Downloading FFMpeg')],
            [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS_BAR-')],
        ]

        # Set the progress bar generator for ffmpeg
        mp4decrypt_download_progress = zip_helper.download_binary_zip(url=helper_scripts.download_links.ffmpeg['DownloadLink'], zip_name=helper_scripts.download_links.ffmpeg['ZipName'])

        # Open up the window and set variable
        window = sg.Window('TPD Crunchy Downloader', progress_bar_layout_ffmpeg, resizable=True, icon=config.assets.icons.taskbar_icon, finalize=True)

        # Set variable for the progress bar
        progress_bar = window['-PROGRESS_BAR-']

        # Start the download and update progress bar
        for progress in mp4decrypt_download_progress:
            progress_bar.update(current_count=(round(progress)))

        # Unzip the binary
        zip_helper.unzip_binary_zip(zip_name=helper_scripts.download_links.ffmpeg['ZipName'], unzip_binary_location=helper_scripts.download_links.ffmpeg['UnzipBinaryLocation'], unzip_folder_location=helper_scripts.download_links.ffmpeg['UnzipFolderLocation'])

        # Close the window once completed
        window.close()

        # return true value for having completed download
        has_ffmpeg = True

    # If ffmpeg is already present, return true
    if os.path.isfile(helper_scripts.download_links.ffmpeg['BinaryLocation']):
        has_ffmpeg = True

    # Return true values for downlods
    return has_nm3u8dlre, has_mp4decrypt, has_ffmpeg