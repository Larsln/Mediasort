import os
from metadata import Metadata
from media_metadata import MediaMetadata
from media_exif_handler import MediaExifHandler
from sorter import Sorter


class FolderCrawler:

    def __init__(self, static_data_loader):
        self.sorter = Sorter(static_data_loader)

    def crawl(self, source_folder):
        # Sicherstellen, dass der Quellordner existiert
        if not os.path.isdir(source_folder):
            raise ValueError(f"Source folder '{source_folder}' does not exist or is not a directory.")

        # Liste der Dateien im aktuellen Ordner
        files = [file for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]
        reference = Metadata()
        reference.source_folder_path = source_folder
        for file in files:

            matching_file = FolderCrawler.has_matching_file(file, files)

            try:
                media_metadata = MediaMetadata(file, source_folder, matching_file)
                self.process_file(media_metadata, reference)

            except TypeError as e:
                print(f"Skipping file '{file}': {e}")
                continue
            try:
                if media_metadata.live_photo:
                    media_metadata = MediaMetadata(matching_file, source_folder)
                    self.process_file(media_metadata, reference)
                    files.remove(matching_file)
            except TypeError as e:
                print(f"Skipping file '{file}': {e}")
                continue



        # Rekursion: Verarbeite alle Unterordner
        subfolders = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]
        for subfolder in subfolders:
            subfolder_path = os.path.join(source_folder, subfolder)
            self.crawl(subfolder_path)

            # Entferne leere Unterordner oder Unterordner mit nur `reference.txt`
            FolderCrawler.delete_empty_folders(subfolder_path)

    def process_file(self, media_metadata, reference):
        if media_metadata.file_path.lower().endswith(
                MediaExifHandler.SUPPORTED_PHOTO_FILES +
                MediaExifHandler.SUPPORTED_VIDEO_FILES):
            media_metadata.set_metadata()
            self.sorter.sort_files(media_metadata, reference)

    @staticmethod
    def has_matching_file(file, file_list):
        base, _ = os.path.splitext(file)
        for other_file in file_list:
            if other_file != file and os.path.splitext(other_file)[0] == base:
                return other_file
        return None

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

    @staticmethod
    def process_media_file(media_metadata, function_used):
        if media_metadata.check_coordinates():
            function_used(media_metadata)
        else:
            if not media_metadata.video and media_metadata.live_photo:
                media_metadata.set_reference(media_metadata.live_photo)
                MediaExifHandler.set_gps_coordinates(media_metadata)
                function_used(media_metadata)
