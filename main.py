# Import dependencies
import helper_scripts

# Check for folders
helper_scripts.folder_helper.check_and_create_folders()

# Check for database
helper_scripts.database_helper.database_check_and_create()

# Check for binaries
has_nm3u8dlre, has_mp4decrypt, has_ffmpeg = helper_scripts.binary_helper.check_and_create_binaries()

# check for cookies
has_cookies = helper_scripts.cookie_helper.check_if_cookies()

# Start the GUI

# Make sure all the prerequisites have been met
if has_nm3u8dlre and has_mp4decrypt and has_ffmpeg and has_cookies:
    helper_scripts.gui_helper.start_gui()