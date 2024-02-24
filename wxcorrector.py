# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com

# TO RUN :

# sudo python wxcorrector.py

import urllib.request
import os


def download_directly(url, destination_path):
    try:
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        print(f"Ensured that the directory {os.path.dirname(destination_path)} exists.")

        # Download the file directly to the destination path
        with urllib.request.urlopen(url) as response, open(
            destination_path, "wb"
        ) as out_file:
            out_file.write(response.read())
            print(f"Successfully downloaded the file to {destination_path}.")

    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")

# URL of the file to download
url = "https://celestrak.org/NORAD/elements/weather.txt"
# Destination path (Ensure the directory exists and you have necessary permissions)
destination_path = "/usr/share/wx/tle/weather.txt"

print("Starting the file download process...")
# Execute the function
download_directly(url, destination_path)
print("File download and copy process completed successfully.")
