from cloudstor import cloudstor
from tqdm import tqdm
import os
import multiprocessing


class CloudstorDownloader:
    def __init__(self, destination_folder, cloudstor_url=None):
        """
        Initializes a CloudstorDownloader object with a destination folder, a Cloudstor URL and a Cloudstor image
        folder.

        :param destination_folder: the folder to download the images to
        :param cloudstor_url: the Cloudstor URL to access
        """
        self.destination_folder = destination_folder
        self.cloudstor_db = cloudstor(url=cloudstor_url, password='')

    def get_subdirectories(self, parent_folder):
        """
        Returns a list of subdirectories in a Cloudstor folder.

        :param parent_folder: the Cloudstor folder to get subdirectories for
        :return: a list of subdirectories
        """
        return [f.rstrip('/') for f in self.cloudstor_db.list(parent_folder) if
                self.cloudstor_db.is_dir(f"{parent_folder}/{f}")]

    def get_files(self, parent_folder, extension=None):
        """
        Returns a list of files in a Cloudstor folder.

        :param parent_folder: the Cloudstor folder to get files for
        :param extension: the extension to filter by
        :return: a list of files
        """
        files = [f for f in self.cloudstor_db.list(parent_folder)]
        if extension is not None:
            files = [f for f in files if f.endswith(extension)]
        return files

    def get_all_files_in_subdirectories(self, parent_folder, extension=None, get_full_path=False):
        """
        Returns a list of files in a Cloudstor folder and all subdirectories.

        :param parent_folder: the Cloudstor folder to get files for
        :param extension: the extension to filter by
        :param get_full_path: whether to return the full path of the file
        :return: a list of files
        """
        subdirectories = self.get_subdirectories(parent_folder)
        files = []
        for subdirectory in subdirectories:
            files.extend(
                [f"{parent_folder}/{subdirectory}/{f}" if get_full_path else f for f in self.get_files(f"{parent_folder}/{subdirectory}", extension=extension)])
        return files

    def get_downloaded_files_in_destination_folder(self, extension=".NEF"):
        """
        Returns a list of downloaded file names in the destination folder.
        """
        if extension is not None:
            return [f for f in os.listdir(self.destination_folder) if f.endswith(extension)]
        else:
            return os.listdir(self.destination_folder)

    def get_files_to_download(self, parent_folder, extension=".NEF", get_full_path=False):
        """
        Returns a list of file names that have not been downloaded yet.

        :param parent_folder: the Cloudstor folder to get files for
        :param extension: the extension to filter by
        :param get_full_path: whether to return the full path of the files
        :return: a list of files
        """
        downloaded_files = self.get_downloaded_files_in_destination_folder(extension=extension)
        all_files = self.get_all_files_in_subdirectories(parent_folder, extension=extension, get_full_path=True)
        files_to_download = [f for f in all_files if f not in downloaded_files]
        if not get_full_path:
            files_to_download = [os.path.basename(f) for f in files_to_download]
        return files_to_download

    def download_file(self, file_name):
        """
        Downloads a single file.

        :param file_name: the full path and file name of the image to download
        """
        # get the file name from the full path
        full_file_path = file_name
        # get the relative path and file name
        file_name = file_name.split('/')[-1]
        # download the file
        try:
            self.cloudstor_db.download_file(full_file_path, os.path.join(self.destination_folder, file_name))
        except Exception as e:
            print(f"Error downloading file {file_name}: {e}")

    def download_files(self, file_list, num_workers=5):
        """
        Downloads a list of files using multiprocessing.

        :param file_list: the list of files to download
        :param num_workers: the number of worker processes to use for downloading
        """
        with multiprocessing.Pool(processes=num_workers) as pool:
            with tqdm(total=len(file_list), desc="Downloading files") as pbar:
                for _ in pool.imap_unordered(self.download_file, file_list):
                    pbar.update()