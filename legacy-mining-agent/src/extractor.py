import zipfile
import urllib.request
import os

def extract_zip(zip_source, extract_to):
    """
    Extracts a local or remote ZIP file to a target directory.
    Supports both file paths and HTTP(S) URLs.
    """
    if zip_source.startswith("http://") or zip_source.startswith("https://"):
        print(f"📥 Downloading ZIP from: {zip_source}")
        zip_path = "temp.zip"
        urllib.request.urlretrieve(zip_source, zip_path)
        downloaded = True
    else:
        print(f"📂 Using local ZIP: {zip_source}")
        zip_path = zip_source
        downloaded = False

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    if downloaded:
        os.remove(zip_path)

    print(f"✅ ZIP extracted to: {extract_to}")
