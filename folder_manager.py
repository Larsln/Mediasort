import os
import shutil


source_folder = "./input"
destination_folder = "./output"

files = os.listdir(source_folder)
files = [f for f in files if os.path.isfile(os.path.join(source_folder, f))]
files.sort()

for file in files:
    print(file)




'''if files:
    # Die erste Datei auswählen
    first_file = files[0]

    # Pfad zur ersten Datei
    source_file_path = os.path.join(source_folder, first_file)

    # Neuen Dateinamen festlegen
    new_file_name = 'reference.png'  # Ändere 'neuer_name.ext' entsprechend

    # Neuer Pfad mit dem neuen Namen
    destination_file_path = os.path.join(destination_folder, new_file_name)

    # Datei verschieben und umbenennen
    shutil.move(source_file_path, destination_file_path)

    print(f"Datei {first_file} wurde in {destination_file_path} umbenannt und verschoben.")
else:
    print("Keine Dateien im Quellordner gefunden.")
'''