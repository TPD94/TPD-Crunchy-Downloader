import shutil
import zipfile
import requests
import os


# Define function to unzip a binary
def unzip_binary_zip(zip_name: str = None, unzip_binary_location: str = None, unzip_folder_location: str = None):

    # Open the zip
    with zipfile.ZipFile(f"{os.getcwd()}/downloads/temp/{zip_name}.zip", 'r') as binary_zip:

        # Extract the contents
        for file in binary_zip.infolist():
            binary_zip.extract(file, path=f'{os.getcwd()}/downloads/temp')

    # Copy the binary over
    shutil.copy2(unzip_binary_location, f"{os.getcwd()}/binaries")

    # Clean up the zip
    os.remove(f"{os.getcwd()}/downloads/temp/{zip_name}.zip")

    # Clean up the extracted folder
    shutil.rmtree(unzip_folder_location)


# Define function to download zip and yield progress percent
def download_binary_zip(url: str = None, zip_name: str = None):

    # Send a get request to the URL
    response = requests.get(url, stream=True)

    # Get the total file size in bytes
    total_size = int(response.headers.get('content-length', 0))

    # Download the file
    with open(f'{os.getcwd()}/downloads/temp/{zip_name}.zip', 'wb') as zip_name:

        # Loop through the download every 1024kb
        for data in response.iter_content(chunk_size=1024):

            # Write the data
            zip_name.write(data)

            # Calculate the percentage progress
            progress_percent = (zip_name.tell() / total_size) * 100

            # Yield the rounded progress percentage
            yield round(progress_percent)




