from os import listdir
from os.path import join
from pathlib import Path

class FolderStructure:

    @staticmethod
    def show_folder_structure_incorrect(sample_path, current_path, root_sample_path, root_current_path):
        print('\n[IMPORT DATA ERROR]: Your folder structure is incorrect')
        short_sample_path = str(Path(sample_path))[len(str(Path(root_sample_path))):]
        if Path(sample_path).is_file():
            print(f'Cannot found file {short_sample_path}')
        if Path(sample_path).is_dir():
            print(f'Cannot found folder {short_sample_path}')
        print('\nCorrect folder structure')
        paths = DisplayablePath.make_tree(Path(root_sample_path))
        for path in paths:
            print(path.displayable())
        print('\nYour folder structure')
        paths = DisplayablePath.make_tree(Path(root_current_path))
        for path in paths:
            print(path.displayable())
        raise SystemExit('')

    @staticmethod
    def check_structure(sample_path, current_path, root_sample_path=None, root_current_path=None):
        if root_sample_path is None:
            root_sample_path = sample_path
        if root_current_path is None:
            root_current_path = current_path
        if Path(sample_path).is_file() != Path(current_path).is_file() or Path(sample_path).is_dir() != Path(current_path).is_dir():
            FolderStructure.show_folder_structure_incorrect(sample_path, current_path, root_sample_path, root_current_path)
        if Path(sample_path).is_dir():
            for sub_sample_path in listdir(Path(sample_path)):
                FolderStructure.check_structure(join(sample_path, sub_sample_path), join(current_path, sub_sample_path), root_sample_path=root_sample_path, root_current_path=root_current_path)