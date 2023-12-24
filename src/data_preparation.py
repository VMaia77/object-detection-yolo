from typing import List, Tuple

import os
from pathlib import Path
from zipfile import ZipFile, BadZipFile
from PIL import Image
from tqdm import tqdm



def prepare_data(zip_path: str, datasets_path: str, old_new_names: List[Tuple]):
    extract_zip_files(zip_path, datasets_path)
    rename_datasets_folders(datasets_path, old_new_names)
    _datasets_path = Path(datasets_path)
    datasets_names = [n[1] for n in old_new_names]
    for d in datasets_names:
        visdrone2yolo(_datasets_path / d)  # convert VisDrone annotations to YOLO labels

def extract_zip_files(zip_path: str, datasets_path: str):
    os.makedirs(datasets_path, exist_ok=True)
    for file_name in os.listdir(zip_path):
        file_path = os.path.join(zip_path, file_name)
        if file_name.endswith('.zip') and os.path.isfile(file_path):
            try:
                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(datasets_path)
                print(f"Successfully extracted: {file_name}")
            except BadZipFile:
                print(f"Error: {file_name} is not a valid zip file.")
    print("Extraction completed.")


def rename_datasets_folders(datasets_path, old_new_names: List[Tuple]):
    for old_new_n in old_new_names:
        train_folder = os.path.join(datasets_path, old_new_n[1])
        os.rename(os.path.join(datasets_path, old_new_n[0]), train_folder)
    print("Rename completed.")


def visdrone2yolo(dataset_path: Path):

    def convert_box(size, box):
        # Convert VisDrone box to YOLO xywh box
        dw = 1. / size[0]
        dh = 1. / size[1]
        return (box[0] + box[2] / 2) * dw, (box[1] + box[3] / 2) * dh, box[2] * dw, box[3] * dh

    (dataset_path / 'labels').mkdir(parents=True, exist_ok=True)  # make labels directory
    pbar = tqdm((dataset_path / 'annotations').glob('*.txt'), desc=f'Converting {dataset_path}')
    for f in pbar:
        img_size = Image.open((dataset_path / 'images' / f.name).with_suffix('.jpg')).size
        lines = []
        with open(f, 'r') as file:  # read annotation.txt
            for row in [x.split(',') for x in file.read().strip().splitlines()]:
                if row[4] == '0':  # VisDrone 'ignored regions' class 0
                    continue
                cls = int(row[5]) - 1
                box = convert_box(img_size, tuple(map(int, row[:4])))
                lines.append(f"{cls} {' '.join(f'{x:.6f}' for x in box)}\n")
                with open(str(f).replace(f'{os.sep}annotations{os.sep}', f'{os.sep}labels{os.sep}'), 'w') as fl:
                    fl.writelines(lines)  # write label.txt