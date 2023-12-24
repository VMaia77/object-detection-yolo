import os
import shutil
import zipfile


def zip_folder(zip_path, folder_path, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    save_in = os.path.join(zip_path, zip_file_name)
    shutil.move(zip_file_name, save_in)
    print(f"The folder {folder_path} has been zipped.")