import os
import re

from metadata import Metadata
from media_metadata import MediaMetadata
from media_exif_handler import MediaExifHandler

class FolderCrawler:

    @staticmethod
    def crawl(source_folder, function_used):
        # Sicherstellen, dass der Quellordner existiert
        if not os.path.isdir(source_folder):
            raise ValueError(f"Source folder '{source_folder}' does not exist or is not a directory.")

        # Liste der Dateien im aktuellen Ordner
        files = [file for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]
        reference = Metadata()
        reference.source_folder_path = source_folder

        for file in files:
            try:
                media_metadata = MediaMetadata(file, source_folder)

                if media_metadata.file_path.lower().endswith(
                        MediaExifHandler.SUPPORTED_PHOTO_FILES +
                        MediaExifHandler.SUPPORTED_VIDEO_FILES):
                    media_metadata.set_metadata()
                    function_used(media_metadata, reference)
            except TypeError as e:
                print(f"Skipping file '{file}': {e}")
                continue

        # Rekursion: Verarbeite alle Unterordner
        subfolders = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]
        for subfolder in subfolders:
            subfolder_path = os.path.join(source_folder, subfolder)
            FolderCrawler.crawl(subfolder_path, function_used)

            # Entferne leere Unterordner oder Unterordner mit nur `reference.txt`
            FolderCrawler.delete_empty_folders(subfolder_path)

    @staticmethod
    def check_live_photos(directory):
        pass

    @staticmethod
    def get_subfolder_names(directory):
        try:
            # Gibt eine Liste aller Unterordner im Verzeichnis zurück
            return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        except FileNotFoundError:
            return []  # Rückgabe einer leeren Liste, falls der Ordner nicht existiert


    @staticmethod
    def delete_empty_folders(subfolder_path):
        try:
            os.rmdir(subfolder_path)
        except OSError:
            if FolderCrawler.check_only_reference_txt(subfolder_path):
                os.remove(os.path.join(subfolder_path, 'reference.txt'))
                os.rmdir(subfolder_path)


    @staticmethod
    def check_only_reference_txt(directory):
        files = os.listdir(directory)
        files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
        return len(files) == 1 and files[0].lower() == 'reference.txt'


