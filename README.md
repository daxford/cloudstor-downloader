# Cloudstor Downloader

A Python package to download files from a Cloudstor folder using the cloudstor module. The package includes methods to download all files in a folder and its subdirectories, filter files by extension, and download files using multiple processes for increased speed.

## Usage

Install the required modules by running:

    pip install -r requirements.txt

To use the package, simply import the CloudstorDownloader class and instantiate an object with a destination folder and a Cloudstor URL:

    from cloudstor_downloader import CloudstorDownloader

    CLOUDSTOR_URL = "example_cloudstor_url"
    CLOUDSTOR_FOLDER = "example_cloudstor_folder"
    DESTINATION_FOLDER = "/path/to/destination/folder"

    cs = CloudstorDownloader(cloudstor_url=CLOUDSTOR_URL, destination_folder=DESTINATION_FOLDER)

To get a list of all files in a Cloudstor folder and its subdirectories, use the get_all_files_in_subdirectories method:

    all_files = cs.get_all_files_in_subdirectories(CLOUDSTOR_FOLDER)

To filter files by extension, pass the desired extension to the extension argument:

    nef_files = cs.get_all_files_in_subdirectories(CLOUDSTOR_FOLDER, extension=".NEF")

To get a list of files that have not yet been downloaded to the destination folder, use the get_files_to_download method:

    nef_files_to_download = cs.get_files_to_download(CLOUDSTOR_FOLDER, extension=".NEF")

To download files to the destination folder, use the download_files method:

    cs.download_files(nef_files_to_download)

You can specify the number of worker processes to use for downloading by passing an integer to the num_workers argument:

    cs.download_files(nef_files_to_download, num_workers=4)

## Requirements

    Python 3.6 or higher
    The cloudstor module (pip install cloudstor)
    The tqdm module (pip install tqdm)
