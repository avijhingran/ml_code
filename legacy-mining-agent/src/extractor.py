import zipfile
import urllib.request
import os

def extract_zip(zip_url, extract_to):
    """
    Downloads and extracts a ZIP file from a given URL into a specified folder.

    Args:
        zip_url (str): Publicly accessible URL of the ZIP file.
        extract_to (str): Directory where the contents will be extracted.
    """
    zip_path = "temp.zip"

    print(f"Downloading ZIP from: {zip_url}")
    urllib.request.urlretrieve(zip_url, zip_path)

    print(f"Extracting to: {extract_to}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    os.remove(zip_path)
    print("ZIP file downloaded and extracted.")
