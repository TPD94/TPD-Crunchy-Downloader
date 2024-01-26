# Import dependencies
from . import download_links
from . import token_helper
import subprocess
import os


# Define the function to generate a command to use with a subprocess
def generate_nm3u8dlre_command(mpd: str = None, download_location: str = None,
                               series_name: str = None, season_number: str = None, episode_number: str =None,
                               episode_title: str = None, resolution: str = None, language: str = None, mp4decryptkeys: list = None):

    n_m3u8dl_re_download_template = [
        f'{download_links.nm3u8dlre["BinaryLocation"]}',
        f'--header',
        f'authorization: {token_helper.get_token()}',
        f'{mpd}',
        '-sv',
        f'res="{resolution[:-1]}*":for=best',
        '-sa',
        f'for=best',
        '--ffmpeg-binary-path',
        f'{download_links.ffmpeg["BinaryLocation"]}',
        '--decryption-binary-path',
        f'{download_links.mp4decrypt["BinaryLocation"]}',
        '--tmp-dir',
        f'{os.getcwd()}/downloads/temp/',
        '--save-dir',
        f'{download_location}',
        '--save-name',
        f'{series_name} - Season {season_number} Episode {episode_number} - {episode_title} - No Subs',
        '--binary-merge',
        'True',
        '--mux-after-done',
        'format=mkv',
        '--log-level',
        'off'
    ] + mp4decryptkeys

    return n_m3u8dl_re_download_template


def run_nm3u8dlre_subprocess_with_output(nm3u8dlre_command: list = None):

    # Set the process
    process = subprocess.Popen(nm3u8dlre_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Read and print stdout in real-time
    while True:

        # Break if done
        if process.stdout.readline() == '' and process.poll() is not None:
            break

        # Yield the line
        yield process.stdout.readline()

    # Ensure the process has completed
    process.communicate()


# Define the function to generate a command to use with a subprocess
def generate_ffmpeg_command(mkv_location: str = None, mkv_name: str = None, mkv_subtitles: list = None):

    ffmpeg_template = [
        f'{download_links.ffmpeg["BinaryLocation"]}',
        f'-i',
        f'{mkv_location}/{mkv_name} - No Subs.mkv',
        ] + mkv_subtitles + [
        f'-c:v',
        f'copy',
        f'-c:a',
        f'copy',
        f'-c:s',
        f'copy',
        f'{mkv_location}/{mkv_name} - With Subs.mkv'
    ]

    return ffmpeg_template