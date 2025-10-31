import xml.etree.ElementTree as et
import os

class AnimationObjectEditor:

    def __init__(self):
        self.tree = None
        self.root = None
        self.namespace = None

    def load_file(self, file_path: str) -> bool:
        """
            Open and load the .caml into memory
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_path = os.path.join(script_dir, file_path)
        try:
            self.tree = et.parse(resolved_path)
            self.root = self.tree.getroot()
            if self.root.tag.startswith('{'):
                self.namespace = self.root.tag.split('}')[0][1:]
            else:
                self.namespace = None
            return True
        except et.ParseError as e:
            print(f'Parsing error: {e}')
            return False
        except FileNotFoundError:
            print(f'File not found: {resolved_path}')
            return False
        except Exception as e:
            print(f'Unexpected error: {e}')
            return False

    def save_file(self, file_path: str) -> bool:
        """
            Don't forget the file path/name
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_path = os.path.join(script_dir, file_path)
        try:
            if self.namespace:
                et.register_namespace('', self.namespace)
            with open(resolved_path, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                self.tree.write(f, encoding='utf-8', xml_declaration=False)
            print(f'File saved: {resolved_path}')
            return True
        except Exception as e:
            print(f'Error saving: {e}')
            return False

    def get_root(self):
        return self.root

    def get_tree(self):
        return self.tree

    def find_target(self, tag_name: str, attr_name: str, attr_value: str):
        if self.namespace:
            query = f'.//{{{self.namespace}}}{tag_name}'
        else:
            query = f'.//{tag_name}'
        for elem in self.root.findall(query):
            if elem.get(attr_name) == attr_value:
                return elem
        return None

    def insert_object_to_target(self, tag_name: str, attr_name: str, attr_value: str, object: et.Element) -> bool:
        """
            Give a name and a tree then it'll do it for you.
        """
        target = self.find_target(tag_name, attr_name, attr_value)
        if target is None:
            print(f"can't find '{tag_name}', {attr_name}={attr_value}")
            return False
        target.append(object)
        print(f"inserted object into '{tag_name}', {attr_name}={attr_value}")
        return True